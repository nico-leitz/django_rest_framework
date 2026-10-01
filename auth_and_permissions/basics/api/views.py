from rest_framework import generics
from basics.models import Manufacturer, Product, ManufacturerUser
from .serializers import ManufacturerSerializer, ProductSerializer, ManufacturerUserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsStaffOrReadOnly, IsAdminForDeleteOrPatchAndReadOnly, IsOwnerOrAdmin

class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    
    # -------------------------------------------------------------------------
    # DIE VIEW ALS CONTROLLER (MVT / MVC-Muster)
    #
    # RÜCKWEG (GET - Daten abrufen):
    # 1. View holt alle Daten aus der DB (queryset).
    # 2. View drückt die Python-Objekte dem Serializer in die Hand.
    # 3. Serializer übersetzt sie in JSON.
    # 4. View schickt das JSON an den Browser.
    #
    # HINWEG (POST - Daten speichern):
    # 1. View empfängt JSON-Daten (SCHRITT 1).
    # 2. View übergibt Daten an Serializer: "Sind die valide?" (is_valid).
    # 3. Wenn gültig, gibt die View den finalen Speicher-Befehl (serializer.save()).
    # -------------------------------------------------------------------------
    serializer_class = ManufacturerSerializer

    # ANTWORT AUF DEINE FRAGEN ZU PERMISSION_CLASSES:
    # 1. Was passiert hier? 
    #    Das ist die Zugangskontrolle (Autorisierung) für diese View. Bevor die View 
    #    überhaupt anfängt, Daten zu holen (GET) oder zu speichern (POST), 
    #    wird geprüft, ob der Nutzer die Rechte dafür hat.
    #
    # 2. Zählt das nur für diese Tabelle in der DB? / Immer für den URL Path?
    #    Es zählt NICHT global für die Tabelle in der Datenbank! Es gilt AUSSCHLIESSLICH 
    #    für den URL-Pfad, der auf diese spezifische View verweist. Wenn du eine andere 
    #    View/URL baust, die auch 'Manufacturer' bearbeitet, musst du die Rechte dort 
    #    erneut festlegen.

    permission_classes = [IsAuthenticated] #IsStaffOrReadOnly


class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    # Was passiert hier?
    # Hier greift deine selbstgeschriebene Custom-Permission aus 'permissions.py'.
    # Da dies eine Detail-View ist (für einzelne Objekte wie /manufacturers/1/),
    # schützt diese Zeile den Endpunkt so: Wahrscheinlich darf hier jeder (oder jeder 
    # eingeloggte) die Details ansehen (ReadOnly), aber nur ein Admin darf 
    # Änderungen vornehmen (Patch) oder das Objekt löschen (Delete).
    # Auch hier gilt: Das schützt nur DIESEN EINEN URL-Endpunkt, nicht die Tabelle an sich.
    permission_classes = [IsAdminForDeleteOrPatchAndReadOnly]


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ManufacturerUserList(generics.ListCreateAPIView):
    queryset = ManufacturerUser.objects.all()
    serializer_class = ManufacturerUserSerializer


class ManufacturerUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ManufacturerUser.objects.all()
    serializer_class = ManufacturerUserSerializer
    permission_classes = [IsOwnerOrAdmin]                          


class ManufacturerProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        manufacturer_id = self.kwargs['manufacturer_id']
        return Product.objects.filter(manufacturer_id=manufacturer_id)

    # EINGRIFF IN SCHRITT 3: DIE VIEW GIBT ZUSÄTZLICHE DATEN MIT
    # Hier greift die View (Controller) noch einmal kurz ein, bevor endgültig gespeichert wird.
    def perform_create(self, serializer):
        # Sie holt die manufacturer_id aus der URL...
        manufacturer_id = self.kwargs['manufacturer_id']
        # ...und drückt sie dem Serializer (dem Arbeiter) beim Speichern in die Hand.
        # Der Serializer übernimmt ab hier wieder und schreibt den Eintrag in die DB.
        serializer.save(manufacturer_id=manufacturer_id)