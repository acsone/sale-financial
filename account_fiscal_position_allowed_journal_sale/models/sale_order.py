# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        """
        If there is a fiscal position in vals and exactly one sale journal
        allowed on it, set this journal in vals.
        """
        res = super()._prepare_invoice()
        fiscal_position_id = res.get("fiscal_position_id")
        if fiscal_position_id:
            fiscal_position_model = self.env["account.fiscal.position"]
            fiscal_position = fiscal_position_model.browse(fiscal_position_id)
            sale_journals = fiscal_position.allowed_journal_ids.filtered(
                lambda j: j.type == "sale"
            )
            if len(sale_journals) == 1:
                res["journal_id"] = sale_journals[0].id
        return res
