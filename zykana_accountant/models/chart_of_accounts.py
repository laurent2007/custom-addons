from odoo import api,fields,models

class ChartOfAccounts(models.Model):
    _name = 'chart.of.accounts'
    _description = '会计科目表'
    #_parent_store = True

    
    coa_name = fields.Char('名称',translate=True,required=True)
    #coa_sequence = fields.Integer('序号')
    coa_code = fields.Char('代码')
    coa_type = fields.Selection(
            [('bankandcash','银行和现金'),
            ('currentassets','流动资产'),
            ('receivable','应收'),
            ('payable','应付'),
            ('currentliabilities','流动负债')],
            '类型')
    coa_china_type = fields.Selection(
            [('asset','资产类'),
            ('liabilities','负债类'),
            ('common','共同类'),
            ('ownersrights','所有者权益类'),
            ('cost','成本类'),
            ('profitloss','损益类')],
            '会计科目分类')
    forwhere = fields.Char('适用范围')
    initial_borrower =  fields.Monetary('期初借方','currency_id')
    initial_lender =  fields.Monetary('期初贷方','currency_id')
    currency_id = fields.Many2one('res.currency') #price helper
    

    active = fields.Boolean('是否启用?',default=True)