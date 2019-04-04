from odoo import api,fields,models

class accountJournalItems(models.Model):
    _name = 'account.journal.items'
    _description = '日记账项目'
    #_parent_store = True

    #_inherit = ['account.journal','account.account','chart.of.accounts']
    
    number = fields.Many2one('account.invoice',string='日记账分录',readonly=True)

    journal_id = fields.Many2one('account.journal',string='日记账',readonly=True)
    
    
    tag = fields.Char('标签')
    reference = fields.Char('参考')
    #business_partner = fields.Char('业务伙伴')
    user_id = fields.Many2one('res.users',string='业务伙伴',readonly=True)
    
    #chart_of_account = fields.Char('科目')
    account_id = fields.Many2one('account.account',string='科目',readonly=True)
    
    
    borrower =  fields.Monetary('借方','currency_id')
    lender =  fields.Monetary('贷方','currency_id')
    currency_id = fields.Many2one('res.currency') #price helper
    
    date_due = fields.Many2one('account.invoice',string='到期日期',readonly=True)
    
    