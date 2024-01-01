/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormLabel } from "@web/views/form/form_label";

FormLabel.defaultProps = {
    color: null
}

patch(FormLabel.prototype,{
    get className() {
        super.className(...arguments);
        console.log(this.props)
    }
})




// odoo.define("mommy_base.form_view", function (require) {
//     'use strict';

//     var FormRenderer = require("web.FormRenderer");

//     FormRenderer.include({
//         _renderTagLabel: function (node) {
//             if (!this.renderInvisible && node.tag === 'field' &&
//                 node.attrs.modifiers.invisible === true) {
//                 // skip rendering of invisible fields/labels
//                 return $();
//             }
//             var self = this;
//             var text;
//             var style;
//             let fieldName;
//             if (node.tag === 'label') {
//                 fieldName = this.fieldIdsToNames[node.attrs.for]; // 'for' references a <field> node id
//             } else {
//                 fieldName = node.attrs.name;
//             }
//             if ('string' in node.attrs) { // allow empty string
//                 text = node.attrs.string;
//             } else if (fieldName) {
//                 text = this.state.fields[fieldName].string;
//             } else {
//                 return this._renderGenericTag(node);
//             }

//             if ('color' in node.attrs){
//                 style = "color:"+ node.attrs.color
//             }
//             var $result = $('<label>', {
//                 class: 'o_form_label',
//                 for: this._getIDForLabel(node.tag === 'label' ? node.attrs.for : node.attrs.id),
//                 text: text,
//                 style: style
//             });
//             if (node.tag === 'label') {
//                 this._handleAttributes($result, node);
//             }
//             var modifiersOptions;
//             if (fieldName) {
//                 modifiersOptions = {
//                     callback: function (element, modifiers, record) {
//                         var widgets = self.allFieldWidgets[record.id];
//                         var widget = _.findWhere(widgets, { name: fieldName });
//                         const fieldsInfo = record.fieldsInfo[self.viewType];
//                         if (!widget) {
//                             if (fieldsInfo[fieldName]) {
//                                 self.labelsToPostProcess.push(element.callback.bind(self, element, modifiers, record));
//                             }
//                             return;
//                         }
//                         element.$el.toggleClass('o_form_label_empty', !!( // FIXME condition is evaluated twice (label AND widget...)
//                             record.data.id
//                             && (modifiers.readonly || self.mode === 'readonly')
//                             && !widget.isSet()
//                         ));
//                     },
//                 };
//             }
//             // FIXME if the function is called with a <label/> node, the registered
//             // modifiers will be those on this node. Maybe the desired behavior
//             // would be to merge them with associated field node if any... note:
//             // this worked in 10.0 for "o_form_label_empty" reevaluation but not for
//             // "o_invisible_modifier" reevaluation on labels...
//             this._registerModifiers(node, this.state, $result, modifiersOptions);
//             return $result;
//         }
//     });

// });