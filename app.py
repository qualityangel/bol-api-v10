import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import csv
from datetime import datetime
from client import Client  # Gebruik de juiste import

# Kleuren uit de afbeelding
LIGHT_BLUE = "#7EDDD8"
BLUE_GREEN = "#39C3AC"
DARK_BLUE_GREEN = "#005F61"
WHITE = "#FFFFFF"
BLACK = "#000000"

class SalesOrderDashboard(ctk.CTk):
    def __init__(self, client):
        super().__init__()

        self.client = client
        self.translations = {
            'en': {
                'title': "Sales Order Dashboard",
                'order_id': "SO ID",
                'order_date': "Order Date",
                'ean': "EAN",
                'quantity': "Quantity",
                'product_name': "Product Name",
                'brand': "Brand",
                'fulfilment_method': "Fulfilment Method",
                'refresh': "Refresh",
                'no_title_warning': "Warning: No title found for EAN {}",
                'no_brand_warning': "Warning: No brand found for EAN {}",
                'csv_not_found': "CSV file not found. No existing orders to load.",
                'search': "Search...",
                'language': "Language",
                'customer_name': "Customer Name",
                'customer_address': "Customer Address",
                'city': "City",
                'postal_code': "Postal Code",
                'country': "Country",
                'billing_name': "Billing Name",
                'billing_address': "Billing Address",
                'billing_city': "Billing City",
                'billing_postal_code': "Billing Postal Code",
                'billing_country': "Billing Country"
            },
            'nl': {
                'title': "Verkooporder Dashboard",
                'order_id': "Order ID",
                'order_date': "Besteldatum",
                'ean': "EAN",
                'quantity': "Aantal",
                'product_name': "Productnaam",
                'brand': "Merk",
                'fulfilment_method': "Verzendmethode",
                'refresh': "Vernieuwen",
                'no_title_warning': "Waarschuwing: Geen titel gevonden voor EAN {}",
                'no_brand_warning': "Waarschuwing: Geen merk gevonden voor EAN {}",
                'csv_not_found': "CSV-bestand niet gevonden. Geen bestaande orders om te laden.",
                'search': "Zoeken...",
                'language': "Taal",
                'customer_name': "Klantnaam",
                'customer_address': "Klantadres",
                'city': "Stad",
                'postal_code': "Postcode",
                'country': "Land",
                'billing_name': "Factuur Naam",
                'billing_address': "Factuur Adres",
                'billing_city': "Factuur Stad",
                'billing_postal_code': "Factuur Postcode",
                'billing_country': "Factuur Land"
            },
            'de': {
                'title': "Verkaufsauftrag Dashboard",
                'order_id': "Auftragsnummer",
                'order_date': "Bestelldatum",
                'ean': "EAN",
                'quantity': "Menge",
                'product_name': "Produktname",
                'brand': "Marke",
                'fulfilment_method': "Versandmethode",
                'refresh': "Aktualisieren",
                'no_title_warning': "Warnung: Kein Titel für EAN {} gefunden",
                'no_brand_warning': "Warnung: Keine Marke für EAN {} gefunden",
                'csv_not_found': "CSV-Datei nicht gefunden. Keine bestehenden Bestellungen zu laden.",
                'search': "Suchen...",
                'language': "Sprache",
                'customer_name': "Kundenname",
                'customer_address': "Kundenadresse",
                'city': "Stadt",
                'postal_code': "Postleitzahl",
                'country': "Land",
                'billing_name': "Rechnungsname",
                'billing_address': "Rechnungsadresse",
                'billing_city': "Rechnungsstadt",
                'billing_postal_code': "Rechnungspostleitzahl",
                'billing_country': "Rechnungsland"
            }
        }

        self.current_language = 'en'

        self.title(self.translations[self.current_language]['title'])
        self.geometry("1024x768")
        self.configure(bg=BLUE_GREEN)

        self.create_widgets()
        self.load_orders_from_csv()  # Laad orders bij het opstarten
        self.load_orders()
        self.update_translations()

    def set_language(self, lang):
        self.current_language = lang
        self.update_translations()

    def create_widgets(self):
        self.button_frame = ctk.CTkFrame(self, fg_color=LIGHT_BLUE)
        self.button_frame.pack(fill=tk.X)

        self.orders_button = ctk.CTkButton(self.button_frame, text="Orders", command=lambda: self.show_frame(self.orders_frame), fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.orders_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.articles_button = ctk.CTkButton(self.button_frame, text="Artikelen", command=lambda: self.show_frame(self.articles_frame), fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.articles_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.messages_button = ctk.CTkButton(self.button_frame, text="Berichten", command=lambda: self.show_frame(self.messages_frame), fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.messages_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.tab1_button = ctk.CTkButton(self.button_frame, text="Tab1", command=lambda: self.show_frame(self.tab1_frame), fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.tab1_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.tab2_button = ctk.CTkButton(self.button_frame, text="Tab2", command=lambda: self.show_frame(self.tab2_frame), fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.tab2_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.language_var = tk.StringVar(value=self.current_language)
        self.language_menu = ctk.CTkOptionMenu(self.button_frame, variable=self.language_var, values=['en', 'nl', 'de'], command=self.change_language, fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.language_menu.pack(side=tk.RIGHT, padx=5, pady=5)

        self.frames = {}
        
        self.orders_frame = ctk.CTkFrame(self, fg_color=LIGHT_BLUE)
        self.articles_frame = ctk.CTkFrame(self, fg_color=LIGHT_BLUE)
        self.messages_frame = ctk.CTkFrame(self, fg_color=LIGHT_BLUE)
        self.tab1_frame = ctk.CTkFrame(self, fg_color=LIGHT_BLUE)
        self.tab2_frame = ctk.CTkFrame(self, fg_color=LIGHT_BLUE)

        self.frames["orders"] = self.orders_frame
        self.frames["articles"] = self.articles_frame
        self.frames["messages"] = self.messages_frame
        self.frames["tab1"] = self.tab1_frame
        self.frames["tab2"] = self.tab2_frame

        for frame in self.frames.values():
            frame.pack(fill=tk.BOTH, expand=True)

        self.create_orders_tab()
        self.create_articles_tab()
        self.create_messages_tab()
        self.create_tab1()
        self.create_tab2()

        self.show_frame(self.orders_frame)  # Toon standaard de Orders-tab

    def show_frame(self, frame):
        for f in self.frames.values():
            f.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

    def change_language(self, lang):
        self.set_language(lang)

    def update_translations(self):
        self.title(self.translations[self.current_language]['title'])
        self.orders_button.configure(text=self.translations[self.current_language]['order_id'])
        self.articles_button.configure(text=self.translations[self.current_language]['product_name'])
        self.messages_button.configure(text=self.translations[self.current_language]['product_name'])
        self.tab1_button.configure(text="Tab1")
        self.tab2_button.configure(text="Tab2")
        self.language_menu.set(self.translations[self.current_language]['language'])
        self.orders_search_entry.configure(placeholder_text=self.translations[self.current_language]['search'])
        self.articles_search_entry.configure(placeholder_text=self.translations[self.current_language]['search'])
        self.messages_search_entry.configure(placeholder_text=self.translations[self.current_language]['search'])
        self.refresh_button.configure(text=self.translations[self.current_language]['refresh'])
        
        # Update treeview headings
        self.orders_tree.heading("SO ID", text=self.translations[self.current_language]['order_id'])
        self.orders_tree.heading("Order Date", text=self.translations[self.current_language]['order_date'])
        self.orders_tree.heading("EAN", text=self.translations[self.current_language]['ean'])
        self.orders_tree.heading("Quantity", text=self.translations[self.current_language]['quantity'])
        self.orders_tree.heading("Product Name", text=self.translations[self.current_language]['product_name'])
        self.orders_tree.heading("Brand", text=self.translations[self.current_language]['brand'])
        self.orders_tree.heading("Fulfilment Method", text=self.translations[self.current_language]['fulfilment_method'])

        self.articles_tree.heading("EAN", text=self.translations[self.current_language]['ean'])
        self.articles_tree.heading("Product Name", text=self.translations[self.current_language]['product_name'])
        self.articles_tree.heading("Brand", text=self.translations[self.current_language]['brand'])

        self.messages_tree.heading("Order ID", text=self.translations[self.current_language]['order_id'])
        self.messages_tree.heading("Name", text=self.translations[self.current_language]['product_name'])  # Gebruik product_name voor 'Naam'

    def create_orders_tab(self):
        self.orders_search_var = tk.StringVar()
        self.orders_search_entry = ctk.CTkEntry(self.orders_frame, textvariable=self.orders_search_var, placeholder_text=self.translations[self.current_language]['search'], fg_color=WHITE, text_color=BLACK)
        self.orders_search_entry.pack(pady=10)
        self.orders_search_entry.bind("<KeyRelease>", self.search_orders)

        self.orders_tree = ttk.Treeview(self.orders_frame, columns=("SO ID", "Order Date", "EAN", "Quantity", "Product Name", "Brand", "Fulfilment Method", "Customer Name", "Customer Address", "City", "Postal Code", "Country"), show="headings")
        self.orders_tree.heading("SO ID", text=self.translations[self.current_language]['order_id'])
        self.orders_tree.heading("Order Date", text=self.translations[self.current_language]['order_date'])
        self.orders_tree.heading("EAN", text=self.translations[self.current_language]['ean'])
        self.orders_tree.heading("Quantity", text=self.translations[self.current_language]['quantity'])
        self.orders_tree.heading("Product Name", text=self.translations[self.current_language]['product_name'])
        self.orders_tree.heading("Brand", text=self.translations[self.current_language]['brand'])
        self.orders_tree.heading("Fulfilment Method", text=self.translations[self.current_language]['fulfilment_method'])
        self.orders_tree.heading("Customer Name", text=self.translations[self.current_language]['customer_name'])
        self.orders_tree.heading("Customer Address", text=self.translations[self.current_language]['customer_address'])
        self.orders_tree.heading("City", text=self.translations[self.current_language]['city'])
        self.orders_tree.heading("Postal Code", text=self.translations[self.current_language]['postal_code'])
        self.orders_tree.heading("Country", text=self.translations[self.current_language]['country'])

        self.orders_tree.pack(fill=tk.BOTH, expand=True)
        self.orders_tree.bind("<Double-1>", self.on_order_click)

        self.refresh_button = ctk.CTkButton(self.orders_frame, text=self.translations[self.current_language]['refresh'], command=self.load_orders, fg_color=DARK_BLUE_GREEN, text_color=WHITE)
        self.refresh_button.pack(pady=10)

    def on_order_click(self, event):
        selected_item = self.orders_tree.selection()
        if selected_item:
            order_id = self.orders_tree.item(selected_item, 'values')[0]
            self.show_order_details(order_id)

    def show_order_details(self, order_id):
        order_details = self.client._order(order_id)
        shipment_details = order_details.get('shipmentDetails', {})
        billing_details = order_details.get('billingDetails', {})

        customer_name = f"{shipment_details.get('firstName', 'N/A')} {shipment_details.get('surname', 'N/A')}"
        customer_address = f"{shipment_details.get('streetName', 'N/A')} {shipment_details.get('houseNumber', 'N/A')} {shipment_details.get('houseNumberExtension', 'N/A')}"
        city = shipment_details.get('city', 'N/A')
        postal_code = shipment_details.get('zipCode', 'N/A')
        country = shipment_details.get('countryCode', 'N/A')

        billing_name = f"{billing_details.get('firstName', 'N/A')} {billing_details.get('surname', 'N/A')}"
        billing_address = f"{billing_details.get('streetName', 'N/A')} {billing_details.get('houseNumber', 'N/A')} {billing_details.get('houseNumberExtension', 'N/A')}"
        billing_city = billing_details.get('city', 'N/A')
        billing_postal_code = billing_details.get('zipCode', 'N/A')
        billing_country = billing_details.get('countryCode', 'N/A')

        details_window = ctk.CTkToplevel(self)
        details_window.title(self.translations[self.current_language]['order_id'] + ": " + order_id)
        details_window.geometry("600x400")

        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['customer_name'] + ": " + customer_name, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['customer_address'] + ": " + customer_address, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['city'] + ": " + city, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['postal_code'] + ": " + postal_code, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['country'] + ": " + country, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['billing_name'] + ": " + billing_name, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['billing_address'] + ": " + billing_address, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['billing_city'] + ": " + billing_city, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['billing_postal_code'] + ": " + billing_postal_code, fg_color=WHITE, text_color=BLACK).pack(pady=10)
        ctk.CTkLabel(details_window, text=self.translations[self.current_language]['billing_country'] + ": " + billing_country, fg_color=WHITE, text_color=BLACK).pack(pady=10)

    def create_articles_tab(self):
        self.articles_search_var = tk.StringVar()
        self.articles_search_entry = ctk.CTkEntry(self.articles_frame, textvariable=self.articles_search_var, placeholder_text=self.translations[self.current_language]['search'], fg_color=WHITE, text_color=BLACK)
        self.articles_search_entry.pack(pady=10)
        self.articles_search_entry.bind("<KeyRelease>", self.search_articles)

        self.articles_tree = ttk.Treeview(self.articles_frame, columns=("EAN", "Product Name", "Brand"), show="headings")
        self.articles_tree.heading("EAN", text=self.translations[self.current_language]['ean'])
        self.articles_tree.heading("Product Name", text=self.translations[self.current_language]['product_name'])
        self.articles_tree.heading("Brand", text=self.translations[self.current_language]['brand'])

        self.articles_tree.pack(fill=tk.BOTH, expand=True)

    def create_messages_tab(self):
        self.messages_search_var = tk.StringVar()
        self.messages_search_entry = ctk.CTkEntry(self.messages_frame, textvariable=self.messages_search_var, placeholder_text=self.translations[self.current_language]['search'], fg_color=WHITE, text_color=BLACK)
        self.messages_search_entry.pack(pady=10)
        self.messages_search_entry.bind("<KeyRelease>", self.search_messages)

        self.messages_tree = ttk.Treeview(self.messages_frame, columns=("Order ID", "Name"), show="headings")
        self.messages_tree.heading("Order ID", text=self.translations[self.current_language]['order_id'])
        self.messages_tree.heading("Name", text=self.translations[self.current_language]['product_name'])  # Gebruik product_name voor 'Naam'

        self.messages_tree.pack(fill=tk.BOTH, expand=True)

    def create_tab1(self):
        ctk.CTkLabel(self.tab1_frame, text="Content for Tab 1", fg_color=WHITE, text_color=BLACK).pack(pady=20)

    def create_tab2(self):
        ctk.CTkLabel(self.tab2_frame, text="Content for Tab 2", fg_color=WHITE, text_color=BLACK).pack(pady=20)

    def search_orders(self, event):
        query = self.orders_search_var.get().lower()
        for item in self.orders_tree.get_children():
            values = self.orders_tree.item(item, "values")
            if any(query in str(value).lower() for value in values):
                self.orders_tree.item(item, tags=('match',))
            else:
                self.orders_tree.item(item, tags=('nomatch',))
        self.orders_tree.tag_configure('match', background=LIGHT_BLUE)
        self.orders_tree.tag_configure('nomatch', background=WHITE)

    def search_articles(self, event):
        query = self.articles_search_var.get().lower()
        for item in self.articles_tree.get_children():
            values = self.articles_tree.item(item, "values")
            if any(query in str(value).lower() for value in values):
                self.articles_tree.item(item, tags=('match',))
            else:
                self.articles_tree.item(item, tags=('nomatch',))
        self.articles_tree.tag_configure('match', background=LIGHT_BLUE)
        self.articles_tree.tag_configure('nomatch', background=WHITE)

    def search_messages(self, event):
        query = self.messages_search_var.get().lower()
        for item in self.messages_tree.get_children():
            values = self.messages_tree.item(item, "values")
            if any(query in str(value).lower() for value in values):
                self.messages_tree.item(item, tags=('match',))
            else:
                self.messages_tree.item(item, tags=('nomatch',))
        self.messages_tree.tag_configure('match', background=LIGHT_BLUE)
        self.messages_tree.tag_configure('nomatch', background=WHITE)

    def load_orders_from_csv(self):
        """Load orders from CSV and display them in the treeview."""
        self.loaded_orders = set()
        try:
            with open("orders.csv", "r", encoding="ANSI") as csvfile:
                reader = csv.reader(csvfile, delimiter=";")
                next(reader)  # Skip header row
                for row in reader:
                    self.orders_tree.insert("", tk.END, values=row)
                    self.loaded_orders.add(row[0])  # Voeg orderID toe aan de set
        except FileNotFoundError:
            print(self.translations[self.current_language]['csv_not_found'])

    def load_orders(self):
        """Fetch orders from the API and update the treeview and CSV file."""
        try:
            orders = self.client._orders()
            output_rows = []

            for order in orders:
                for order_item in order['orderItems']:
                    orderID = order['orderId']
                    besteldatum = order['orderPlacedDateTime']
                    eannummer = order_item['ean']
                    aantal = order_item['quantity']
                    Verzendmethode = order_item['fulfilmentMethod']
                    if Verzendmethode == "FBR":
                        Verzendmethode = "VVB"

                    products = self.client._product(eannummer)

                    naam = None
                    beschrijving = None
                    for attribute in products.get('attributes', []):
                        if attribute['id'] == 'Title':
                            naam = attribute['values'][0]['value']
                        elif attribute['id'] == 'Description':
                            beschrijving = attribute['values'][0]['value']

                    if naam is None or naam == "":
                        print(self.translations[self.current_language]['no_title_warning'].format(eannummer))

                    merk = None
                    for party in products.get('parties', []):
                        if party['type'] == 'Brand' and party['role'] == 'BRAND':
                            merk = party['name']
                            break
                    if not merk:
                        merk = "Merkloos"
                        print(self.translations[self.current_language]['no_brand_warning'].format(eannummer))

                    # Haal klantgegevens op
                    order_details = self.client._order(orderID)
                    shipment_details = order_details.get('shipmentDetails', {})
                    customer_name = f"{shipment_details.get('firstName', 'N/A')} {shipment_details.get('surname', 'N/A')}"
                    customer_address = f"{shipment_details.get('streetName', 'N/A')} {shipment_details.get('houseNumber', 'N/A')} {shipment_details.get('houseNumberExtension', '')}"
                    city = shipment_details.get('city', 'N/A')
                    postal_code = shipment_details.get('zipCode', 'N/A')
                    country = shipment_details.get('countryCode', 'N/A')

                    billing_details = order_details.get('billingDetails', {})
                    billing_name = f"{billing_details.get('firstName', 'N/A')} {billing_details.get('surname', 'N/A')}"
                    billing_address = f"{billing_details.get('streetName', 'N/A')} {billing_details.get('houseNumber', 'N/A')} {billing_details.get('houseNumberExtension', '')}"
                    billing_city = billing_details.get('city', 'N/A')
                    billing_postal_code = billing_details.get('zipCode', 'N/A')
                    billing_country = billing_details.get('countryCode', 'N/A')

                    if orderID not in self.loaded_orders:  # Controleer of orderID al is geladen
                        output_row = [orderID, besteldatum, eannummer, aantal, naam, merk, Verzendmethode, customer_name, customer_address, city, postal_code, country]
                        output_rows.append(output_row)
                        self.orders_tree.insert("", tk.END, values=output_row)
                        self.loaded_orders.add(orderID)  # Voeg orderID toe aan de set

            with open("orders.csv", "a", newline="", encoding="ANSI") as output_file:
                writer = csv.writer(output_file, delimiter=";")
                if output_file.tell() == 0:
                    writer.writerow(["OrderID", "BestelDatum", "EanNummer", "Aantal", "Product", "Merk", "Verzendmethode", "Customer Name", "Customer Address", "City", "Postal Code", "Country"])
                writer.writerows(output_rows)
                
        except Exception as e:
            print(f"Failed to load orders: {e}")

    def order_bestaat(self, orderID):
        try:
            with open('orders.csv', 'r', encoding="ANSI") as csvfile:
                reader = csv.reader(csvfile, delimiter=";")
                next(reader)
                for row in reader:
                    if row[0] == orderID:
                        return True
        except FileNotFoundError:
            return False
        return False

if __name__ == "__main__":
    client_id = "Your-ID"
    client_secret = "Your-secret"
    client = Client(client_id, client_secret)
    
    app = SalesOrderDashboard(client)
    app.mainloop()
