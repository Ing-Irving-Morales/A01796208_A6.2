import json
import os

class FileHandler:
    """Handles reading and writing to files with error handling."""
    
    @staticmethod
    def save_data(filename, data):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([obj.__dict__ for obj in data], f, indent=4)
        except IOError as e:
            print(f"Error saving data to {filename}: {e}")

    @staticmethod
    def load_data(filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # Req 5: Handle invalid data, display error and continue
            print(f"Error reading {filename}: {e}. Starting with empty list.")
            return []

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def display_info(self):
        return f"ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"

class Hotel:
    def __init__(self, hotel_id, name, location, rooms_available):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms_available = int(rooms_available)

    def display_info(self):
        return f"ID: {self.hotel_id}, Name: {self.name}, Loc: {self.location}, Rooms: {self.rooms_available}"

    def reserve_room(self):
        if self.rooms_available > 0:
            self.rooms_available -= 1
            return True
        return False

    def cancel_reservation(self):
        self.rooms_available += 1

class Reservation:
    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def display_info(self):
        return f"ResID: {self.reservation_id}, CustID: {self.customer_id}, HotelID: {self.hotel_id}"

class HotelManager:
    FILE = 'hotels.json'
    hotels = []

    @classmethod
    def load_hotels(cls):
        data = FileHandler.load_data(cls.FILE)
        cls.hotels = []
        for item in data:
            try:
                cls.hotels.append(Hotel(**item))
            except TypeError:
                print(f"Skipping invalid hotel record: {item}")

    @classmethod
    def save_hotels(cls):
        FileHandler.save_data(cls.FILE, cls.hotels)

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        cls.load_hotels()
        if any(h.hotel_id == hotel_id for h in cls.hotels):
            print(f"Hotel {hotel_id} already exists.")
            return False
        new_hotel = Hotel(hotel_id, name, location, rooms)
        cls.hotels.append(new_hotel)
        cls.save_hotels()
        return new_hotel

    @classmethod
    def delete_hotel(cls, hotel_id):
        cls.load_hotels()
        original_count = len(cls.hotels)
        cls.hotels = [h for h in cls.hotels if h.hotel_id != hotel_id]
        if len(cls.hotels) < original_count:
            cls.save_hotels()
            return True
        return False

    @classmethod
    def display_hotel(cls, hotel_id):
        cls.load_hotels()
        for hotel in cls.hotels:
            if hotel.hotel_id == hotel_id:
                print(hotel.display_info())
                return hotel.display_info()
        print("Hotel not found.")
        return None

    @classmethod
    def modify_hotel(cls, hotel_id, name=None, location=None, rooms=None):
        cls.load_hotels()
        for hotel in cls.hotels:
            if hotel.hotel_id == hotel_id:
                if name: hotel.name = name
                if location: hotel.location = location
                if rooms: hotel.rooms_available = rooms
                cls.save_hotels()
                return True
        return False

    @classmethod
    def find_hotel(cls, hotel_id):
        cls.load_hotels()
        for hotel in cls.hotels:
            if hotel.hotel_id == hotel_id:
                return hotel
        return None

class CustomerManager:
    FILE = 'customers.json'
    customers = []

    @classmethod
    def load_customers(cls):
        data = FileHandler.load_data(cls.FILE)
        cls.customers = []
        for item in data:
            try:
                cls.customers.append(Customer(**item))
            except TypeError:
                print(f"Skipping invalid customer record: {item}")

    @classmethod
    def save_customers(cls):
        FileHandler.save_data(cls.FILE, cls.customers)

    @classmethod
    def create_customer(cls, customer_id, name, email):
        cls.load_customers()
        if any(c.customer_id == customer_id for c in cls.customers):
            print(f"Customer {customer_id} already exists.")
            return False
        new_cust = Customer(customer_id, name, email)
        cls.customers.append(new_cust)
        cls.save_customers()
        return new_cust

    @classmethod
    def delete_customer(cls, customer_id):
        cls.load_customers()
        original_count = len(cls.customers)
        cls.customers = [c for c in cls.customers if c.customer_id != customer_id]
        if len(cls.customers) < original_count:
            cls.save_customers()
            return True
        return False

    @classmethod
    def display_customer(cls, customer_id):
        cls.load_customers()
        for cust in cls.customers:
            if cust.customer_id == customer_id:
                print(cust.display_info())
                return cust.display_info()
        print("Customer not found.")
        return None

    @classmethod
    def modify_customer(cls, customer_id, name=None, email=None):
        cls.load_customers()
        for cust in cls.customers:
            if cust.customer_id == customer_id:
                if name: cust.name = name
                if email: cust.email = email
                cls.save_customers()
                return True
        return False

class ReservationManager:
    FILE = 'reservations.json'
    reservations = []

    @classmethod
    def load_reservations(cls):
        data = FileHandler.load_data(cls.FILE)
        cls.reservations = []
        for item in data:
            try:
                cls.reservations.append(Reservation(**item))
            except TypeError:
                print(f"Skipping invalid reservation record.")

    @classmethod
    def save_reservations(cls):
        FileHandler.save_data(cls.FILE, cls.reservations)

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        # Check if customer exists
        CustomerManager.load_customers()
        if not any(c.customer_id == customer_id for c in CustomerManager.customers):
            print("Customer not found.")
            return False

        # Check if hotel exists and update room count
        hotel = HotelManager.find_hotel(hotel_id)
        if not hotel:
            print("Hotel not found.")
            return False

        if hotel.reserve_room():
            HotelManager.save_hotels() # Save updated room count
            
            cls.load_reservations()
            new_res = Reservation(reservation_id, customer_id, hotel_id)
            cls.reservations.append(new_res)
            cls.save_reservations()
            return new_res
        else:
            print("No rooms available.")
            return False

    @classmethod
    def cancel_reservation(cls, reservation_id):
        cls.load_reservations()
        res_to_cancel = None
        for res in cls.reservations:
            if res.reservation_id == reservation_id:
                res_to_cancel = res
                break
        
        if res_to_cancel:
            # Restore room count
            hotel = HotelManager.find_hotel(res_to_cancel.hotel_id)
            if hotel:
                hotel.cancel_reservation()
                HotelManager.save_hotels()
            
            cls.reservations.remove(res_to_cancel)
            cls.save_reservations()
            return True
        return False