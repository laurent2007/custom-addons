from odoo import api,fields,models,exceptions

class Checkout(models.Model):
    _name='library.checkout'
    _description = 'Checkout Request'
    _inherit = ['mail.thread','mail.activity.mixin']

    member_id = fields.Many2one('library.member',required=True)
    user_id = fields.Many2one('res.users','Librarian',default = lambda s: s.env.uid)
    request_date = fields.Date(default =lambda s :fields.Date.today())
    line_ids = fields.One2many('library.checkout.line','checkout_id',string='Borrowed Books', )

    @api.model
    def _default_stage(self):
        Stage = self.env['library.checkout.stage']
        return Stage.search([],limit=1)
    @api.model
    def _group_expand_stage_id(self,stages,domain,order):
        return stages.search([],order=order)

    stage_id = fields.Many2one(
            'library.checkout.stage',
            default=_default_stage,
            group_expand='_group_expand_stage_id'
            )
    state = fields.Selection(related='stage_id.state')

    checkout_date = fields.Date(readonly=True)
    closed_date= fields.Date(readonly=True)
    member_image = fields.Binary(related='member_id.partner_id.image')
    num_other_checkouts = fields.Integer(
            compute='_compute_num_other_checkouts')
    num_books = fields.Integer(compute='_compute_num_books')
    
    priority = fields.Selection(
            [('0','Low'),
             ('1','Normal'),
             ('2','High')],
            'Priority',
            default='1')
    kanban_state = fields.Selection(
            [('normal','In Progress'),
             ('blocked','Blocked'),
             ('done','Ready for next stage')],
            'kanban State',
            default='normal')

    color = fields.Integer('Color Index')


    @api.onchange('member_id')
    def onchange_member_id(self):
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = today
        #return True
            
    @api.model
    def create(self,vals):
        #code before create: should use the vals dict
        if 'stage_id' in vals:
            Stage = self.env['library.checkout.stage']
            new_stage = Stage.browse(vals['stage_id']).state
            if new_stage == 'open':
                vals['checkout_date'] = fields.Date.today()
        new_record = super().create(vals)
        # code after create: can use the  new_recored created
        if new_record.state == 'done':
            raise exceptions.UserError('Not allowed to create a checkout in the done state')
        return new_record

    @api.multi
    def write(self,vals):
        #code before write: can use 'self',with the old values
        if 'stage_id' in vals:
            Stage = self.env['library.checkout.stage']
            new_state = Stage.browse(vals['stage_id']).state
            if new_state == 'open' and self.state != 'open':
                vals['checkout_date'] = fields.Date.today()
            if new_state == 'done' and self.state != 'done':
                vals['close_date'] = fields.Date.today()
        super().write(vals)
        # code after write: can use 'self' ,with the updated values
        return True


    def button_done(self):
        Stage = self.env['library.checkout.stage']
        done_stage = Stage.search(
                        [('state','=','done')],limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True

    def _compute_num_other_checkouts(self):
        for rec in self:
            domain = [
                   ('member_id','=',rec.member_id.id),
                   ('state','in',['open']),
                   ('id','!=',rec.id)]
            rec.num_other_checkouts = self.search_count(domain)

    @api.depends('line_ids')
    def _compute_num_books(self):
        for book in self:
            book.num_books = len(book.line_ids)

class CheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'
    checkout_id = fields.Many2one('library.checkout')
    book_id = fields.Many2one('library.book')
