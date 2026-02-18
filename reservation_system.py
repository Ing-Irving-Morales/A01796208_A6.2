'''Actividad 6.2 '''

import json
import os
import unittest

# Definición de clases
class FileHandler:
    '''Clase para leer json con manejo de errores'''
    
    @staticmethod
    def save_data(filename, data):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump([obj.__dict__ for obj in data], file, indent=4)
        except IOError as e:
            print(f"Error al guardar los datos en {filename}: {e}")

    @staticmethod
    def load_data(filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al leer {filename}: {e}. El archivo está vacío")
            return []

class Customer:
    '''Clase para el cliente'''
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def display_info(self):
        return f"ID: {self.customer_id}, Nombre: {self.name}, Email: {self.email}"

class Hotel:
    '''Clase para el hotel'''
    def __init__(self, hotel_id, name, location, rooms_available):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms_available = int(rooms_available)

    def display_info(self):
        return f"ID: {self.hotel_id}, Nombre: {self.name}, Ubicación: {self.location}, Habitaciones: {self.rooms_available}"

    def reserve_room(self):
        if self.rooms_available > 0:
            self.rooms_available -= 1
            return True
        return False

    def cancel_reservation(self):
        self.rooms_available += 1

class Reservation:
    '''Clase para la reservación'''
    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def display_info(self):
        return f"Reservation: {self.reservation_id}, Cliente: {self.customer_id}, Hotel: {self.hotel_id}"

#************************
#Métodos para interactuar con las clases anteriores

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
                print(f"Saltando registro ínvalido de hotel: {item}")

    @classmethod
    def save_hotels(cls):
        FileHandler.save_data(cls.FILE, cls.hotels)

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        cls.load_hotels()
        if any(h.hotel_id == hotel_id for h in cls.hotels):
            print(f"El Hotel {hotel_id} ya existe")
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
        print("Hotel no encontrado")
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
                print(f"Saltando registro ínvalido de cliente: {item}")

    @classmethod
    def save_customers(cls):
        FileHandler.save_data(cls.FILE, cls.customers)

    @classmethod
    def create_customer(cls, customer_id, name, email):
        cls.load_customers()
        if any(c.customer_id == customer_id for c in cls.customers):
            print(f"Cliente {customer_id} ya existe")
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
        print("Cliente no encontrado")
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
                print(f"Saltando registro ínvalido de reservación: {item}")

    @classmethod
    def save_reservations(cls):
        FileHandler.save_data(cls.FILE, cls.reservations)

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        # Se requiere revisar la existencia del cliente
        CustomerManager.load_customers()
        if not any(c.customer_id == customer_id for c in CustomerManager.customers):
            print("Cliente no encontrado")
            return False

        # Se requiere revisar si el hotel existe y hay reservación
        hotel = HotelManager.find_hotel(hotel_id)
        if not hotel:
            print("Hotel no encontrado")
            return False

        if hotel.reserve_room():
            HotelManager.save_hotels()
            
            cls.load_reservations()
            new_res = Reservation(reservation_id, customer_id, hotel_id)
            cls.reservations.append(new_res)
            cls.save_reservations()
            return new_res
        else:
            print("No hay habitaciones disponibles")
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
            # Si se cancela la reservación se actualiza la cuenta de habitaciones disponibles
            hotel = HotelManager.find_hotel(res_to_cancel.hotel_id)
            if hotel:
                hotel.cancel_reservation()
                HotelManager.save_hotels()
            
            cls.reservations.remove(res_to_cancel)
            cls.save_reservations()
            return True
        return False

# Sección de testing

class TestHotelSystem(unittest.TestCase):
    def setUp(self):
        '''Se resetean todas las variables para que el testing corra bien'''
        self.hotel_file = 'hotels.json'
        self.cust_file = 'customers.json'
        self.res_file = 'reservations.json'
        
        for f in [self.hotel_file, self.cust_file, self.res_file]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
             for f in [self.hotel_file, self.cust_file, self.res_file]:
                if os.path.exists(f):
                    os.remove(f)

    # Pruebas para el Hotel
    def test_create_hotel(self):
        h = HotelManager.create_hotel("H1", "Hotel de Prueba", "Ciudad A", 10)
        self.assertEqual(h.name, "Hotel de Prueba")
        self.assertTrue(os.path.exists(self.hotel_file))

    def test_create_duplicate_hotel(self):
        HotelManager.create_hotel("H1", "Hotel 1", "Ciudad A", 10)
        result = HotelManager.create_hotel("H1", "Hotel 2", "Ciudad B", 5)
        self.assertFalse(result)

    def test_display_hotel(self):
        HotelManager.create_hotel("H1", "Mostrar Hotel", "Ciudad A", 5)
        info = HotelManager.display_hotel("H1")
        self.assertIn("Mostrar Hotel", info)
        self.assertIsNone(HotelManager.display_hotel("H99"))

    def test_modify_hotel(self):
        HotelManager.create_hotel("H1", "Nombre anterior", "Ciudad A", 5)
        HotelManager.modify_hotel("H1", name="Nuevo nombre", rooms=20)
        h = HotelManager.find_hotel("H1")
        self.assertEqual(h.name, "Nuevo nombre")
        self.assertEqual(h.rooms_available, 20)
        self.assertFalse(HotelManager.modify_hotel("H99"))

    def test_delete_hotel(self):
        HotelManager.create_hotel("H1", "Borrar Hotel", "Ciudad A", 5)
        self.assertTrue(HotelManager.delete_hotel("H1"))
        self.assertFalse(HotelManager.delete_hotel("H1")) # Already deleted

    # Pruebas para los hoteles
    def test_create_customer(self):
        c = CustomerManager.create_customer("C1", "Irving Morales", "a01796208@tec.mx")
        self.assertEqual(c.email, "a01796208@tec.mx")

    def test_create_duplicate_customer(self):
        CustomerManager.create_customer("C1", "Irving", "irving@tec.mx")
        self.assertFalse(CustomerManager.create_customer("C1", "Ivan", "irvingn@tec.mx"))

    def test_modify_customer(self):
        CustomerManager.create_customer("C1", "Irving", "irving@tec.mx")
        CustomerManager.modify_customer("C1", email="ing_irving@tec.mx")
        # Reload to verify persistence
        CustomerManager.load_customers()
        self.assertEqual(CustomerManager.customers[0].email, "irving@tec.mx")
        self.assertFalse(CustomerManager.modify_customer("C99"))

    def test_delete_customer(self):
        CustomerManager.create_customer("C1", "Irving", "irving@tec.mx")
        self.assertTrue(CustomerManager.delete_customer("C1"))
        self.assertFalse(CustomerManager.delete_customer("C99"))

    def test_display_customer(self):
        CustomerManager.create_customer("C1", "Irving", "irving@tec.mx")
        info = CustomerManager.display_customer("C1")
        self.assertIn("Irving", info)
        self.assertIsNone(CustomerManager.display_customer("C99"))

    # Pruebas para la reservación
    def test_create_reservation_success(self):
        HotelManager.create_hotel("H1", "Reservación del Hotel", "Ciudad", 2)
        CustomerManager.create_customer("C1", "Reservación del cliente", "cliente@tec.mx")
        
        res = ReservationManager.create_reservation("R1", "C1", "H1")
        self.assertIsNotNone(res)
        
        # Se verifica que las habitaciones disponibles dismuyan cuando se reserva una habitación
        h = HotelManager.find_hotel("H1")
        self.assertEqual(h.rooms_available, 1)

    def test_create_reservation_failure(self):
        # No existe el cliente
        HotelManager.create_hotel("H1", "Hotel", "Ciudad", 2)
        self.assertFalse(ReservationManager.create_reservation("R1", "C99", "H1"))
        
        # No existe el hotel
        CustomerManager.create_customer("C1", "Cliente", "cliente@tec.mx")
        self.assertFalse(ReservationManager.create_reservation("R1", "C1", "H99"))

        # No hay habitaciones disponibles
        HotelManager.create_hotel("H2", "Hotel Lleno", "Ciudad", 0)
        self.assertFalse(ReservationManager.create_reservation("R2", "C1", "H2"))

    def test_cancel_reservation(self):
        HotelManager.create_hotel("H1", "Cancelación del Hotel", "Ciudad", 1)
        CustomerManager.create_customer("C1", "Cancelación del cliente", "cliente@tec.mx")
        ReservationManager.create_reservation("R1", "C1", "H1")
        
        # Cancelación
        self.assertTrue(ReservationManager.cancel_reservation("R1"))
        
        # Se verifica que las habitaciones disponibles se actualicen
        h = HotelManager.find_hotel("H1")
        self.assertEqual(h.rooms_available, 2)
        
        # No se pudo cancelar la reservación porque no existe
        self.assertFalse(ReservationManager.cancel_reservation("R99"))

    # Pruebas para el manejo de datos inválidos
    def test_invalid_data_handling(self):
        # Se hace la prueba con un archivo de hoteles
        with open(self.hotel_file, 'w') as f:
            f.write("{ invalid json }")
        
        # Se demuestra que el programa continua
        HotelManager.load_hotels()
        self.assertEqual(len(HotelManager.hotels), 0)

if __name__ == '__main__':
    unittest.main()