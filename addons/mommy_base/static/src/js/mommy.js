/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";
import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { registry } from "@web/core/registry";

const userMenuRegistry = registry.category("user_menuitems");

patch(WebClient.prototype,{
    async setup() {
        super.setup();
        let data = await this.env.services.rpc("/web/dataset/call_kw/ir.config_parameter/get_param", {
            model: "ir.config_parameter",
            method: "get_param",
            args: ["mommy.title"],
            kwargs: {}
        })
        this.title.setParts({ zopenerp: data })
    }
});

patch(UserMenu.prototype,{
    async setup(){
        super.setup();
        let data = await this.env.services.rpc('/web/dataset/call_kw/ir.config_parameter/get_personal_center', {
            "model": "res.config.settings",
            "method": "get_personal_center",
            "args": [],
            "kwargs":{}
        });
        let [doc, sup, short, acc] = data;
        if(!doc){
            userMenuRegistry.remove("documentation");
        }
        if(!sup){
            userMenuRegistry.remove("support");
        }
        if(!short){
            userMenuRegistry.remove("shortcuts");
        }
        if(!acc){
            userMenuRegistry.remove("odoo_account");
        }

    }
});
