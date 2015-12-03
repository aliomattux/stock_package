from openerp.osv import osv, fields
from openerp.tools.translate import _

class StockCreateManualPackage(osv.osv_memory):
    _name = 'stock.create.manual.package'
    _columns = {
	'picking': fields.many2one('stock.picking', 'Delivery Order'),
	'qty': fields.integer('Number of Packages'),
    }


    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
	res = {}
	picking_ids = context.get('active_ids')
	if picking_ids:
	    res['picking'] = picking_ids[0]

        return res


    def create_manual_package(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0])
	if wizard.qty < 1:
            raise osv.except_osv(_('User Error!'), _('You have to have at least 1 package!'))
	picking = wizard.picking
	vals = {
		'picking': picking.id,
		'sale': picking.sale.id or False,
	}

	package_obj = self.pool.get('stock.out.package')
	return package_obj.create(cr, uid, vals)
