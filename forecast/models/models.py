# -*- coding: utf-8 -*-

#Course Model

from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import Warning,ValidationError

class forecast(models.Model):
     _name = 'forecast.forecast'

     name = fields.Char(string="Title",required=True)
     
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()
     states = fields.Selection(
            [('draft','Draft'),
             ('confirm','Confirmed'),
             ('cancel','Cancelled'),
             ('done','Done')],
             default='draft',
            )
     
     responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)
     
     session_ids=fields.One2many('forecast.session','course_id',string="Sessions")
     
     
     @api.multi
     def copy(self,default=None):
          default = dict(default or {})
          copied_count = self.search_count(
               [('name','=like',u"Copy of {}%".format(self.name))])
               
          if not copied_count:
               new_name = u"Copy of {}".format(self.name)
          else:
               new_name = u"Copy of {} ({})".format(self.name,copied_count)
          default['name'] = new_name
          default['states'] = 'draft'
          return super(forecast,self).copy(default)
          
          
          

     _sql_constraints = [
          ('name_description_check',
           'CHECK(name != description)',
           "The title of the course should not be the description"),
          ('name_unique',
           'UNIQUE(name)',
           "The course title must be unique"),
     ]
        


     @api.depends('value')
     def _value_pc(self):
         self.value2 = float(self.value) / 100

     @api.multi
     def confirm_state(self):
          for forecast in self:
               self.states = "confirm"
               
               
class Session(models.Model):
     _name = 'forecast.session'
     _description = 'forecast Session'
     
     name = fields.Char(required=True)
     start_date = fields.Date(default=fields.Date.today)
     
     duration = fields.Float(digits=(6,2),help="Duration in days")
     seats = fields.Integer(string="Number of Seats")
     active = fields.Boolean(default=True)
     
     color = fields.Integer()
     
     instructor_id = fields.Many2one('res.partner', string="Instructor",
                                     domain=['|',('instructor','=',True),('category_id.name','ilike',"Teacher")])
     
     course_id = fields.Many2one('forecast.forecast',
        ondelete='cascade', string="Course", required=True)
     
     attendee_ids = fields.Many2many('res.partner', string="Attendees")
     
     taken_seats = fields.Float(string="Taken Seats",compute="_taken_seats")
     
     end_date = fields.Date(string="End Date",store=True,compute="_get_end_date",inverse="_set_end_date")
     
     attendees_count = fields.Integer(string="Attendees Count",compute="_compute_attendees_count",store=True)
     
     @api.depends('attendee_ids')
     def _compute_attendees_count(self):
          for r in self:
               r.attendees_count = len(r.attendee_ids)
          
     
     @api.depends('start_date','duration')
     def _get_end_date(self):
          for r in self:
               if not (r.duration and r.start_date):
                    r.end_date = r.start_date
                    continue
               
               # Add duration to start_date, but: Monday + 5 days = Saturday, so
               # subtract one second to get on Friday instead     
               duration = timedelta(days = r.duration ,seconds = -1)
               r.end_date = r.start_date + duration
     
     
     def _set_end_date(self):
          for r in self:
               if not (r.start_date and r.end_date):
                    continue
               
               # Compute the difference between dates, but: Friday - Monday = 4 days,
               # so add one day to get 5 days instead
               r.duration = (r.end_date - r.start_date).days + 1
     
     
     @api.depends('attendee_ids','seats')
     def _taken_seats(self):
          for r in self:
               if not r.seats:
                    r.taken_seats = 0.0
               else:
                    r.taken_seats = len(r.attendee_ids) / r.seats * 100.0
                    
     @api.onchange('attendee_ids','seats')
     def _verify_validate_seats(self):
          if self.seats < 0:
               return {
                    'warning':{
                              'title':"Incorrept 'seats' value",
                              'message':"The number of available seats may not be negative",
                         },
               }
          if self.seats < len(self.attendee_ids):
               return {
                    'warning':{
                              'title':"Too Many attendees",
                              'message':"Increase seats or remove excess attendees",
                         },
               }
          
     @api.constrains('instructor_id','attendee_ids')
     def _check_instructor_not_in_attendee(self):
          for r in self:
               if r.instructor_id and r.instructor_id in r.attendee_ids:
                    raise exceptions.ValidationError("A session's instructor can't be an attendee")
          
     
          