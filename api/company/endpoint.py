from flask import jsonify, request
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
from api.parse_json import * #for json arg parsing

class manageCompany(Resource):
    def get(self, _company_name_): # get all info about a company #
        try:
            x = company_data.query.filter_by(company_name=_company_name_).first()
            _company_id = x.company_id
            _company_name = x.company_name
            _street = x.street
            _city = x.city
            _state = x.state
            _zip = x.zip
            _phone_number = x.phone_number
            _poc = x.poc
            _authinfo = x.authinfo
            _sites = x.sites

            if x != None:
                return jsonify(
                    response = 200,
					message = 'Company search success',
                    company_id = _company_id,
                    company_name = _company_name,
                    street = _street,
                    city = _city,
                    zip = _zip,
                    phone_number = _phone_number,
					poc = _poc,
                    authinfo = _authinfo,
                    sites = _sites
                )
            else:
                return {
                        'response' : 400,
                        'message' : 'Company search failure'
                       }
        except Exception as e:
            return {'response' : 400}
    
    def put(self, _company_name_): # update a company's info #
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Name of company for account', location='json')
            parser.add_argument('street', type=str, help='street for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Phone_number for account', location='json')
            parser.add_argument('poc', type=json_encode, help='Point Of Contact List for account', location='json')
            parser.add_argument('authinfo', type=json_encode, help='Authentication info for account', location='json')
            parser.add_argument('sites', type=json_encode, help='List of divisions for account', location='json')
            args = parser.parse_args()
            
            if args['company_id'] != None:
                _company_id = args['company_id']
            if args['company_name'] != None:
                _company_name = args['company_name']
            if args['street'] != None:
                _street = args['street']
            if args['city'] != None:
                _city = args['city']
            if args['state'] != None:
                _state = args['state']
            if args['zip'] != None:
                _zip = args['zip']
            if args['phone_number'] != None:
                _phone_number = args['phone_number']
            if args['poc'] != None:
                _poc = args['poc']
            if args['authinfo'] != None:
                _authinfo = args['authinfo']
            if args['sites'] != None:
                _sites = args['sites']
            
            try:
                curr_session = db.session #open database session
                x = company_data.query.filter_by(company_name=_company_name_).first() #fetch the name to be updated
                x.company_id = _company_id   #update the row
                x.company_name = _company_name
                x.street = _street
                x.city = _city
                x.state = _state
                x.zip = _zip
                x.phone_number = _phone_number
                x.poc = json_decode(_poc)
                x.authinfo = json_decode(_authinfo)
                x.sites = json_decode(_sites)
                curr_session.commit() #commit changes
                
                return  {
                            'response' : 200,
                            'message' : 'Company update successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Company update failure'
                        }
        except Exception as e:
            return {'response' : 400}
        
    def delete(self, _company_name_): # delete a company #
        try:
            curr_session = db.session #open database session
            x = company_data.query.filter_by(company_name=_company_name_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return  {
                            'response' : 200,
                            'message' : 'Company delete successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Company delete failure'
                        }
        except Exception as e:
            return {'response' : 400}

class manageCompanyList(Resource):
    def get(self, _company_name_=None): # _company_name_ is optional param #
        URL = request.url
		
        # get a list of sites for specified company #
        if URL.find("api/company") > 0 and URL.find("sites") > 0 and _company_name_ != None:
            try: 
                x = company_data.query.filter_by(company_name=_company_name_).first()
                if x != None:
                    return jsonify(
                        response = 200,
                        sites = x.sites
                    )
                else:
                    return {
                            'response' : 400,
                            'message' : 'Company sites for specified company are not available'
                           }
            except Exception as e:
                return {'response' : 400}
            
        # get list of all sites for all companies #
        elif URL.find("api/company/sites") > 0 and _company_name_ == None:
            try: # .load_only("company_name")
                x = company_data.query.all()
                if x != None:
                    co_site_dict = {}
                    for co in x:
                        co_site_dict[co.company_name] = co.sites
                    return jsonify(
                        response = 200,
                        company_sites = co_site_dict
                    )
                else:
                    return {
                            'response' : 400,
                            'message' : 'Company sites are not available'
                           }
            except Exception as e:
                return {'response' : 400}

		# get a list of poc's for specified company #
        if URL.find("api/company") > 0 and URL.find("poc") > 0 and _company_name_ != None:
            try: 
                x = company_data.query.filter_by(company_name=_company_name_).first()
                if x != None:
                    return jsonify(
                        response = 200,
                        poc = x.poc
                    )
                else:
                    return {
                            'response' : 400,
                            'message' : 'Company POCs for specified company are not available'
                           }
            except Exception as e:
                return {'response' : 400}
            
        # get list of all poc's for all companies #
        elif URL.find("api/company/poc") > 0 and _company_name_ == None:
            try: # .load_only("company_name")
                x = company_data.query.all()
                if x != None:
                    co_poc_dict = {}
                    for co in x:
                        co_poc_dict[co.company_name] = co.poc
                    return jsonify(
                        response = 200,
                        all_company_poc = co_poc_dict
                    )
                else:
                    return {
                            'response' : 400,
                            'message' : 'Company POCs are not available'
                           }
            except Exception as e:
                return {'response' : 400}
            
        # get a list of all companies #
        elif URL.find("api/company") > 0 and _company_name_ == None:
            try: 
                x = company_data.query.with_entities(company_data.company_name).all()
               
                if x != None:
                    companyList = []
                    for co in x:
                        companyList.append(co[0])
                    return jsonify(
                        response = 200,
                        companies = companyList
                    )
                else:
                    return {
                            'response' : 400,
                            'message' : 'Company names are not available'
                           }
            except Exception as e:
                return {'response' : 400}
            
        else:
            return {
                    'response' : 404,
                    'message' : 'Redirection error, route is not available'
                   }
    
    # add to list / create new company #
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Company name for account', location='json')
            parser.add_argument('street', type=str, help='street for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Company_id for account', location='json')
            parser.add_argument('poc', type=json_encode, help='Point Of Contact for account', location='json')
            parser.add_argument('authinfo', type=json_encode, help='Authentication settings for account', location='json')
            parser.add_argument('sites', type=json_encode, help='List of divisions for account', location='json')
            args = parser.parse_args()
            
            _company_id = args['company_id']
            _company_name = args['company_name']
            _street = args['street']
            _city = args['city']
            _state = args['state']
            _zip = args['zip']
            _phone_number = args['phone_number']
            _poc = args['poc']
            _authinfo = args['authinfo']
            _sites = args['sites']
            
            query = company_data(company_id=_company_id, company_name=_company_name, street=_street, 
                              city=_city, state=_state, zip=_zip, phone_number=_phone_number, poc=json_decode(_poc),
							  authinfo=json_decode(_authinfo), sites=json_decode(_sites))
            
            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                            'response' : 200,
                            'message' : 'Company creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Company creation failure'
                        }
        except Exception as e:
            return {'response' : 400}
