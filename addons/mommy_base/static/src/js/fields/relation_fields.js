// odoo.define("mommy_base.relation_fields", function (require) {
//     // 'use strict';

//     // const RelationFields = require("web.relational_fields");
//     // const Core = require("web.core");
//     // const _t = Core._t;
//     // const X2Many = RelationFields.FieldX2Many;

//     // X2Many.include({
//     //     init: function (parent, name, record, options) {
//     //         this._super.apply(this, arguments);
//     //         self.createText = self.attrs['add-label'] || _t('Add');
//     //         self.operations = [];
//     //         self.isReadonly = self.mode === 'readonly';
//     //         self.view = self.attrs.views[self.attrs.mode];
//     //         self.isMany2Many = self.field.type === 'many2many' || self.attrs.widget === 'many2many';
//     //         self.activeActions = {};
//     //         self.recordParams = { fieldName: self.name, viewType: self.viewType };
//     //         // The limit is fixed so it cannot be changed by adding/removing lines in
//     //         // the widget. It will only change through a hard reload or when manually
//     //         // changing the pager (see _onPagerChanged).
//     //         self.pagingState = {
//     //             currentMinimum: self.value.offset + 1,
//     //             limit: self.value.limit,
//     //             size: self.value.count,
//     //             validate: () => {
//     //                 // TODO: we should have some common method in the basic renderer...
//     //                 return self.view.arch.tag === 'tree' ?
//     //                     self.renderer.unselectRow() :
//     //                     Promise.resolve();
//     //             },
//     //             withAccessKey: false,
//     //         };

//     //         var arch = self.view && self.view.arch;
//     //         if (arch) {
//     //             self.activeActions.create = arch.attrs.create ?
//     //                 !!JSON.parse(arch.attrs.create) :
//     //                 true;
//     //             self.activeActions.delete = arch.attrs.delete ?
//     //                 !!JSON.parse(arch.attrs.delete) :
//     //                 true;
//     //             self.editable = arch.attrs.editable;
//     //             self._canQuickEdit = false;

//     //         } else {
//     //             self._canQuickEdit = false;
//     //         }

//     //         self._computeAvailableActions(record);
//     //         if (self.attrs.columnInvisibleFields) {
//     //             self._processColumnInvisibleFields();
//     //         }
//     //     }
//     // });
// });