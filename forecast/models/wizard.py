# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'forecast.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"


    def _default_sessions(self):
        return self.env['forecast.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('forecast.session',
        string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.multi
    def subscribe(self):
        #self.session_id.attendee_ids |= self.attendee_ids
        #return {}
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}