// odoo.define("mommy_base.BasicModel", function (require) {
//     'use strict';

//     var BasicModel = require("web.BasicModel");

//     BasicModel.include({
//         _makeDataPoint: function (params) {
//             var type = params.type || ('domain' in params && 'list') || 'record';
//             var res_id, value;
//             var res_ids = params.res_ids || [];
//             var data = params.data || (type === 'record' ? {} : []);
//             var context = params.context;
//             var fields = _.extend({
//                 display_name: { type: 'char' },
//                 id: { type: 'integer' },
//                 quick_editable: { type: 'boolean' }
//             }, params.fields);

//             const groupedBy = params.groupedBy || [];
//             let isM2MGrouped = false;
//             if (type === 'record') {
//                 res_id = params.res_id || (params.data && params.data.id);
//                 if (res_id) {
//                     data.id = res_id;
//                 } else {
//                     res_id = _.uniqueId('virtual_');
//                 }
//                 // it doesn't make sense for a record datapoint to have those keys
//                 // besides, it will mess up x2m and actions down the line
//                 context = _.omit(context, ['orderedBy', 'group_by']);
//             } else {
//                 var isValueArray = params.value instanceof Array;
//                 res_id = isValueArray ? params.value[0] : undefined;
//                 value = isValueArray ? params.value[1] : params.value;
//                 isM2MGrouped = groupedBy.some((group) => {
//                     const [fieldName] = group.split(':');
//                     return fields[fieldName].type === "many2many";
//                 });
//             }

//             var dataPoint = {
//                 _cache: type === 'list' ? {} : undefined,
//                 _changes: null,
//                 _domains: {},
//                 _rawChanges: {},
//                 aggregateValues: params.aggregateValues || {},
//                 context: context,
//                 count: params.count || res_ids.length,
//                 data: data,
//                 domain: params.domain || [],
//                 fields: fields,
//                 fieldsInfo: params.fieldsInfo,
//                 groupedBy,
//                 groupsCount: 0,
//                 groupsLimit: type === 'list' && params.groupsLimit || null,
//                 groupsOffset: 0,
//                 id: `${params.modelName}_${++this.__id}`,
//                 isM2MGrouped,
//                 isOpen: params.isOpen,
//                 limit: type === 'record' ? 1 : (params.limit || Number.MAX_SAFE_INTEGER),
//                 loadMoreOffset: 0,
//                 model: params.modelName,
//                 offset: params.offset || (type === 'record' ? _.indexOf(res_ids, res_id) : 0),
//                 openGroupByDefault: params.openGroupByDefault,
//                 orderedBy: params.orderedBy || [],
//                 orderedResIDs: params.orderedResIDs,
//                 parentID: params.parentID,
//                 rawContext: params.rawContext,
//                 ref: params.ref || res_id,
//                 relationField: params.relationField,
//                 res_id: res_id,
//                 res_ids: res_ids,
//                 specialData: {},
//                 _specialDataCache: {},
//                 static: params.static || false,
//                 type: type,  // 'record' | 'list'
//                 value: value,
//                 range: params.range,
//                 viewType: params.viewType,
//             };

//             // _editionViewType is a dict whose keys are field names and which is populated when a field
//             // is edited with the viewType as value. This is useful for one2manys to determine whether
//             // or not a field is readonly (using the readonly modifiers of the view in which the field
//             // has been edited)
//             dataPoint._editionViewType = {};

//             dataPoint.evalModifiers = this._evalModifiers.bind(this, dataPoint);
//             dataPoint.getContext = this._getContext.bind(this, dataPoint);
//             dataPoint.getDomain = this._getDomain.bind(this, dataPoint);
//             dataPoint.getFieldNames = this._getFieldNames.bind(this, dataPoint);
//             dataPoint.isDirty = this.isDirty.bind(this, dataPoint.id);
//             dataPoint.isNew = this.isNew.bind(this, dataPoint.id);

//             this.localData[dataPoint.id] = dataPoint;

//             return dataPoint;
//         },

//         _fetchRecord: function (record, options) {
//             var self = this;
//             options = options || {};
//             var fieldNames = options.fieldNames || record.getFieldNames(options);
//             fieldNames = _.uniq(fieldNames.concat(['display_name', 'quick_editable']));
//             return this._rpc({
//                 model: record.model,
//                 method: 'read',
//                 args: [[record.res_id], fieldNames],
//                 context: _.extend({ bin_size: true }, record.getContext()),
//             })
//                 .then(function (result) {
//                     if (result.length === 0) {
//                         return Promise.reject();
//                     }
//                     result = result[0];
//                     record.data = _.extend({}, record.data, result);
//                 })
//                 .then(function () {
//                     self._parseServerData(fieldNames, record, record.data);
//                 })
//                 .then(function () {
//                     return Promise.all([
//                         self._fetchX2Manys(record, options),
//                         self._fetchReferences(record, options)
//                     ]).then(function () {
//                         return self._postprocess(record, options);
//                     });
//                 });
//         },
//     });
// });