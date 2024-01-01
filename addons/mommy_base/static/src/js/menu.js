odoo.define("mommy_base.menu", function (require) {
    'use strict';

    var AbstractWebClient = require("web.AbstractWebClient");
    var UserMenu = require("web.UserMenu");
    var rpc = require("web.rpc");

    AbstractWebClient.include({
        init: function (parent) {
            let self = this;
            this._super.apply(this, arguments);
            rpc.query({
                "model": "ir.config_parameter",
                "method": "get_param",
                "args": ["mommy.title"]
            }).then((title) => {
                if (title) {
                    this.set('title_part', { "zopenerp": title });
                }
            });

        }
    });

    UserMenu.include({
        renderElement: function () {
            this._super.apply(this, arguments);
            var self = this;
            rpc.query({
                "model": "res.config.settings",
                "method": "get_personal_center",
                "args": []
            }).then((res) => {
                let [doc, sup, short, acc] = res
                if (!doc) {
                    self.$("a[data-menu='documentation']").remove();
                }
                if (!sup) {
                    self.$("a[data-menu='support']").remove();
                }
                if (!short) {
                    self.$("a[data-menu='shortcuts']").remove();
                }
                if (!acc) {
                    self.$("a[data-menu='account']").remove();
                }
                if ([doc, sup, short].every((x) => !Boolean(x))) {
                    self.$el.find(".dropdown-divider").remove();
                }
            });
        }
    });
});