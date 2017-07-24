from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# Common Gateway Interface
import cgi

# Import CRUD operations
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a session and connect to DB
from database_setup import database_engine_string

engine = create_engine(database_engine_string)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Provide a form for creating a new restaurant.
            if self.path.endswith("/restaurants/new"):
                # Send response headers.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Create the form.
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' " \
                          "enctype='multipart/form-data' action='/restaurants/new'>" \
                          "<input name='newRestaurantName' type='text' " \
                          "placeholder='New Restaurant Name'>" \
                          "<input type='submit' value='Create'>" \
                          "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            # Provide a form for editing the name of a restaurant.
            if self.path.endswith("/edit"):
                # Retrieve the restaurant ID from the path.
                restaurantID = self.path.split("/")[2]
                # Issue a query to retrieve the restaurant.
                myRestaurantQuery = session.query(Restaurant) \
                    .filter_by(id=restaurantID).one()
                if myRestaurantQuery != []:
                    # Send response headers.
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # Create the form.
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % myRestaurantQuery.name
                    output += "<form method='POST' " \
                              "enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantID
                    output += "<input name='newRestaurantName' type='text' " \
                              "placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>" \
                              "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return
            # Provide a form for deleting a restaurant.
            if self.path.endswith("/delete"):
                # Retrieve the restaurant ID from the path.
                restaurantID = self.path.split("/")[2]
                # Issue a query to retrieve the restaurant.
                myRestaurantQuery = session.query(Restaurant) \
                    .filter_by(id=restaurantID).one()
                if myRestaurantQuery != []:
                    # Send response headers.
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # Create the form.
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name
                    # TODO: Can this form have a different `enctype`?
                    output += "<form method='POST' " \
                              "enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantID
                    output += "<input type='submit' value='Delete'>" \
                              "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return
            # Print all restaurant names on the "/restaurants" page
            if self.path.endswith("/restaurants"):
                # Retrieve all restaurants in the database.
                restaurants = session.query(Restaurant).all()
                # Send response headers.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                # Add a link for creating new restaurants (/restaurants/new).
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a></br></br>"
                # Print all restaurants in DB.
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Add links for editing and deleting elements.
                    output += "<a href='restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href='restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/hello"):
                # This is a successful GET request.
                self.send_response(200)
                # We are responding with HTML.
                self.send_header('Content-type', 'text/html')
                # Send a blank line to indicate the end of HTTP headers.
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' " \
                          "enctype='multipart/form-data' action='/hello'>" \
                          "<h2>What would you like me to say?</h2>" \
                          "<input name='message' type='text'>" \
                          "<input type='submit' value='Submit'>" \
                          "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/hola"):
                # This is a successful GET request.
                self.send_response(200)
                # We are responding with HTML.
                self.send_header('Content-type', 'text/html')
                # Send a blank line to indicate the end of HTTP headers.
                self.end_headers()

                output = ""
                output += "<html><body>&#161Hola! " \
                          "<a href='/hello'>Back to Hello</a>"
                output += "<form method='POST' " \
                          "enctype='multipart/form-data' action='/hello'>" \
                          "<h2>What would you like me to say?</h2>" \
                          "<input name='message' type='text'>" \
                          "<input type='submit' value='Submit'>" \
                          "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
        try:
            # Handle edits to restaurant names.
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    # Retrieve the restaurant ID from the path.
                    restaurantID = self.path.split("/")[2]
                    # Issue a query to retrieve the restaurant.
                    myRestaurantQuery = session.query(Restaurant) \
                        .filter_by(id=restaurantID).one()
                    if myRestaurantQuery != []:
                        # Update the restaurant name in the database.
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        # HTTP Headers
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        # Redirect to the restaurants list page.
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                return
            # Handle restaurant deletions.
            if self.path.endswith("/delete"):
                # TODO: Remove these commented lines of code if unneeded.
                # ctype, pdict = cgi.parse_header(
                #     self.headers.getheader('content-type'))
                # if ctype == 'multipart/form-data':
                # Retrieve the restaurant ID from the path.
                restaurantID = self.path.split("/")[2]
                # Issue a query to retrieve the restaurant.
                myRestaurantQuery = session.query(Restaurant) \
                    .filter_by(id=restaurantID).one()
                if myRestaurantQuery != []:
                    # Delete this restaurant.
                    session.delete(myRestaurantQuery)
                    session.commit()
                    # HTTP Headers
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # Redirect to the restaurants list page.
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return
            # Handle restaurant creations.
            if self.path.endswith("restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    # Create a new Restaurant class.
                    new_restaurant = Restaurant(name=messagecontent[0])
                    session.add(new_restaurant)
                    session.commit()
                    # HTTP Headers
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # Redirect to the restaurants list page.
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return
            if self.path.endswith("/hello"):
                # HTTP Headers
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    output = ""
                    output += "<html><body>"
                    output += " <h2> Okay, how about this: </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += "<form method='POST' " \
                              "enctype='multipart/form-data' action='/hello'>" \
                              "<h2>What would you like me to say?</h2>" \
                              "<input name='message' type='text'>" \
                              "<input type='submit' value='Submit'>" \
                              "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C enetered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
