// odoo.define("mommy_base.form", function (require) {
//     'use strict';

//     var FormView = require("web.FormView");
//     var rpc = require("web.rpc");

//     FormView.include({
//         init: function (viewInfo, params) {
//             this._super.apply(this, arguments);
//             if (params.activeActions) {
//                 this.controllerParams.activeActions = params.activeActions;
//             }
//         },

//         _setSubViewLimit: function (attrs) {
//             var view = attrs.views && attrs.views[attrs.mode];
//             var limit = view && view.arch.attrs.limit && parseInt(view.arch.attrs.limit, 10);
//             rpc.query({
//                 route: "/web/dataset/call_kw/ir.config_parameter/get_param",
//                 params: {
//                     model: "ir.config_parameter",
//                     method: "get_param",
//                     args: ["mommy.x2many.pagesize"],
//                     kwargs: {}
//                 }
//             }).then(function (result) {
//                 attrs.limit = limit || attrs.Widget.prototype.limit || parseInt(result) || 40;
//             });
//         },
//     });

// });