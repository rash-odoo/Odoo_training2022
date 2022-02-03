from operator import truediv
from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError


# estate prioperty type class add property type
class EstatePropertyType(models.Model): 
    _name = 'estate.property.type'
    _description = 'Estate property Type'

    name = fields.Char(string="Property Type", default="Unknown", required=True)
    #property_ids = fields.One2many('estate.property','property_type_id')

# estate property offer class add property offer
class EstatePropertyoffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refuse', 'Refused')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    def action_accepted(self):
        for record in self:
            record.status = 'accepted'
    def action_refused(self):
        for record in self:
            record.status = 'refuse'

#inherit res partner 
class ResPartner(models.Model):
    _inherit = 'res.partner'

    buyer_property_id = fields.One2many('estate.property', 'buyer_id')
    is_buyer = fields.Boolean()


class ResUser(models.Model):
    _inherit = "res.users"

    property_id = fields.One2many('estate.property', 'salesman_id')
    is_buyer=fields.Boolean()

# add estate property tag
class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'

    name = fields.Char(string="Property tag", default="Unknown", required=True)

# add new class my property 
class Myproperty(models.Model):
    _name = 'my.property'
    _description = 'My property'

    name = fields.Char()
  
    partner_id = fields.Many2one('res.partner')


# add class estate property
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'This module will add a record to store details'

    # in description show curret user 
    def get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name +'\'s property'


    name = fields.Char(string="Name", default="Unknown", required=True)
    description = fields.Text(default= get_description)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    image = fields.Image()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
        ])
    property_type_id = fields.Many2one('estate.property.type')
    property_tag_ids = fields.Many2many('estate.property.tag')
    total_area = fields.Integer(compute='_compute_area',inverse='_inverse_area')
    salesman_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')
    # best_price = fields.Float(compute="_compute_best_price", store=True)
    # validity = fields.Integer(default=7)
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new')
  
    #compute & inverse method
    @api.depends('living_area','garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2


    # add constraints
    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")

    # show all record
    def open_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "views": [[view_id, 'tree']],
            # "res_id": 2,
            "target": "new",
            "domain": [('property_id', '=', self.id)]
        }
    # show confirm record 
    def confirm_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "views": [[view_id, 'tree']],
            "target": "new",
            "domain": [('status', '=', 'accepted')]
        }
    #it is used in sold or cancel button to check property is sold or cancel
    def action_sold(self):
        for record in self:
           if record.state == 'cancel':
                raise UserError("Cancel Property cannot be sold")
           record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold Property cannot be canceled")
            record.state = 'cancel'

    #it perform when user is interface with some action
    @api.onchange('garden')
    def _check_garden(self):
        for record in self:
            if record . garden:
                record.garden_area=10
                record.garden_orientation='north'
            else:
                record.garden_area=None
                record.garden_orientation=None

    #it is used to create update and delete record
    @api.model
    def create(self,vals):
        vals = {'name': 'Azure', 'expected_price':'300000'}
        res = super(EstateProperty, self).create(vals)
        return res
 
    def write(self,vals):
        print("\n write method is call",vals)
        res =  super(EstateProperty, self).write(vals)
        return res


    def unlink(self):
        print("\nDelete method is    call")
        res =  super(EstateProperty, self).unlink()
        return res