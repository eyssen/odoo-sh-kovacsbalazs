# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, date, time, timedelta

import logging
_logger = logging.getLogger(__name__)





class HrEmployee(models.Model):
    
    _inherit = "hr.employee"
    
    
    auto_attendance = fields.Boolean(u'Automatikus munkaidőbeosztás')
    wage_ids = fields.One2many('hr.employee.wage', 'employee_id', u'Teljesítménybér elszámolások', readonly=True)
    guru_attendance = fields.Boolean(u'Szerepeljen a Guru jelenlétiben?')
    basic_wage = fields.Float(u'Személyi alapbér')
    balance_previous = fields.Float(u'Az előző hónap végi teljesítménybér egyenlege', readonly=True)
    balance_start = fields.Float(u'Korábbról áthozott induló teljesítménybér egyenlege', readonly=True)
    wage_7day = fields.Float(u'Előző 7 napban jóváhagyott teljesítménybér', compute='_compute_wage', readonly=True)
    wage_month = fields.Float(u'Tárgyhóban jóváhagyott teljesítménybér', compute='_compute_wage', readonly=True)
    wage_hold = fields.Float(u'Jóváhagyásra váró teljesítménybér', compute='_compute_wage', readonly=True)
    wage_multiplier = fields.Float(u'Teljesítménybér szorzó', required=True, default=1)


    def _compute_wage(self):
        self.ensure_one()
        
        if self.user_id:

            WageS = self.env['project.task.wage'].search([('user_id', '=', self.user_id.id),('date_accounted', '>=', date.today() - timedelta(days=7))])
            sum = 0
            for Wage in WageS:
                sum += Wage.amount
            self.wage_7day = sum
            
            WageS = self.env['project.task.wage'].search([('user_id', '=', self.user_id.id),('date_accounted', '>=', date.today().replace(day=1))])
            sum = 0
            for Wage in WageS:
                sum += Wage.amount
            self.wage_month = sum
            
            WageS = self.env['project.task.wage'].search([('user_id', '=', self.user_id.id),('state', '=', 'open')])
            sum = 0
            for Wage in WageS:
                sum += Wage.amount
            self.wage_hold = sum


    def create_auto_attendance(self):
        
        employeeS = self.env['hr.employee'].search([('auto_attendance', '!=', False)])
        if employeeS:
            for employee in employeeS:
                leaveS = self.env['hr.leave'].search([
                    ('employee_id', '=', employee.id),
                    ('state', '=', 'validate'),
                    ('request_date_from', '<=', fields.Date.today()),
                    ('request_date_to', '>=', fields.Date.today())
                ])
                globalleaveS = self.env['resource.calendar.leaves'].search([
                    ('date_from', '<=', fields.Date.today()),
                    ('date_to', '>=', fields.Date.today())
                ])
                if not leaveS and not globalleaveS:
                    attendanceS = self.env['hr.attendance'].search([
                        ('employee_id', '=', employee.id),
                        ('check_in', '>=', str(fields.Date.today()) + ' 00:00:00'),
                        ('check_in', '<=', str(fields.Date.today()) + ' 23:59:59')
                    ])
                    if not attendanceS:
                        if employee.resource_calendar_id:
                            resourceCalendarAttendanceS = self.env['resource.calendar.attendance'].search([
                                ('calendar_id', '=', employee.resource_calendar_id.id),
                                ('dayofweek', '=', datetime.today().weekday()),
                                ('date_from', '=', False),
                                ('date_to', '=', False)
                            ])
                            if resourceCalendarAttendanceS:
                                for resourceCalendarAttendance in resourceCalendarAttendanceS:
                                    #TODO: ide majd automatikusan kell az időzónát hozzárendelni
                                    self.env['hr.attendance'].create({
                                        'employee_id': employee.id,
                                        'check_in': datetime.strptime(str(fields.Date.today()), '%Y-%m-%d') + timedelta(seconds=(resourceCalendarAttendance.hour_from * 3600)) - timedelta(hours=2),
                                        'check_out': datetime.strptime(str(fields.Date.today()), '%Y-%m-%d') + timedelta(seconds=(resourceCalendarAttendance.hour_to * 3600)) - timedelta(hours=2)
                                    })


    def advisory_performance_wage_report(self):
        
        EmployeeS = self.env['hr.employee'].search([])
        for Employee in EmployeeS:
            if Employee.wage_7day > 0 or Employee.wage_month > 0 or Employee.wage_hold:
                self.env.ref('kozbeszguru.advisory_performance_wage').with_context().send_mail(Employee.id, force_send=True)





class HrEmployeeWage(models.Model):
    
    _name = 'hr.employee.wage'


    company_id = fields.Many2one('res.company', 'Company', index=True)
    employee_id = fields.Many2one('hr.employee', readonly=True)
    date = fields.Date(u'Elszámolás időpontja', default=fields.Date.today(), readonly=True)
    state = fields.Selection([('creating', 'Creating'), ('created', 'Created')], default='creating', readonly=True)
    wage_ids = fields.One2many('project.task.wage', 'employee_wage_id', u'Elszámolás sorok', readonly=True)
    sum = fields.Float(u'A tárgyhó szerinti teljesítmény egyenlege', readonly=True, store=True)
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', string="Currency", readonly=True)
    accounting_period_start = fields.Date(u'Elszámolási időszak kezdete', readonly=True)
    accounting_period_end = fields.Date(u'Elszámolási időszak vége', readonly=True)
    previous_sum = fields.Float(u'Az előző hónap végi teljesítménybér egyenlege', readonly=True)
    grand_total = fields.Float(u'A Munkavállaló tárgyhavi teljesítménybére', readonly=True)
    basic_wage = fields.Float(u'A Munkavállaló tárgyhavi személyi alapbére', readonly=True)
    payable = fields.Float(u'A Munkavállaló részére tárgyhónapban fizetendő bruttó bér összege', readonly=True)
    next_base = fields.Float(u'A következő hónapnál figyelembe veendő hónap végi teljesítménybér egyenlege', readonly=True)
    active = fields.Boolean('Active', default=True)
    
    
    def _compute_currency(self):
        self.ensure_one()
        #TODO: ide majd valami más kell
        self.currency_id = 11

