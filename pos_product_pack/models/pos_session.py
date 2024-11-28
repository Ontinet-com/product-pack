# Copyright 2024 Dixmit (https://www.dixmit.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from itertools import groupby

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result["search_params"]["fields"].append("pack_ok")
        result["search_params"]["fields"].append("pack_line_ids")
        result["search_params"]["fields"].append("pack_type")
        result["search_params"]["fields"].append("pack_component_price")
        return result

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append("product.pack.line")
        return result

    def _loader_params_product_pack_line(self):
        return {
            "search_params": {
                "domain": [("parent_product_id.available_in_pos", "=", True)],
                "fields": ["parent_product_id", "quantity", "product_id"],
            },
        }

    def _get_pos_ui_product_pack_line(self, params):
        return self.env["product.pack.line"].search_read(
            **params["search_params"]
        )
