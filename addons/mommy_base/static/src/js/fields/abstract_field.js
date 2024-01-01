// odoo.define("mommy_base.basic_fields", function (require) {
//     'use strict';

//     var AbstractField = require("web.AbstractField");
//     var rpc = require("web.rpc");


//     AbstractField.include({

//         start :function(){
//             var result = this._super(...arguments);
//             this._canQuickEdit = this.record.data.quick_editable;
//             console.log('******abstract field****')
//             console.log(this)
//             return result
//         }
//     });
// });