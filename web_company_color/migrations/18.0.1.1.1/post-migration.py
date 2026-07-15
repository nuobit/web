# Copyright NuoBiT Solutions - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Regenerate the per-company color attachments in the current format.

    Databases upgraded from older versions still carry the color
    attachments in the legacy format (raw SCSS content, mimetype
    ``application/octet-stream``). The current module compiles the SCSS
    server-side and serves the attachment URL directly as a stylesheet,
    so it needs compiled CSS with mimetype ``text/css`` — browsers refuse
    the legacy attachments under strict MIME checking and company colors
    silently stop applying. Only the ``post_init_hook`` (fresh installs)
    regenerates them; upgrades never did. Idempotent: regenerating an
    up-to-date attachment rewrites it with identical semantics.
    """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["res.company"].search([]).scss_create_or_update_attachment()
