import json

from .services.content import ContentService


def site_context(request):
    service = ContentService()
    restaurant = service.restaurant()
    path = request.path.rstrip("/") or "/"
    page_seo = {
        "/": {
            "title": "Rumah Makan Padang Bateh Kota | Masakan Padang Bandung",
            "description": "Rumah Makan Padang Bateh Kota di Rajawali Barat, Andir, Bandung. Nikmati nasi Padang, rendang, ayam, ikan, gulai, menu satuan, dan paket hemat.",
        },
        "/menu": {
            "title": "Menu Rumah Makan Padang Bandung | Bateh Kota Rajawali",
            "description": "Lihat daftar menu Rumah Makan Padang Bateh Kota Rajawali Bandung: nasi komplit, rendang, ayam, ikan, gulai, lauk satuan, dan paket hemat.",
        },
        "/gallery": {
            "title": "Galeri Rumah Makan Padang Bateh Kota Bandung",
            "description": "Lihat galeri dan sajian Rumah Makan Padang Bateh Kota di Rajawali Barat, Andir, Bandung.",
        },
        "/lokasi": {
            "title": "Lokasi Rumah Makan Padang Bateh Kota | Rajawali Barat Bandung",
            "description": "Temukan alamat, jam buka, nomor WhatsApp, dan petunjuk lokasi Rumah Makan Padang Bateh Kota di Rajawali Barat, Andir, Bandung.",
        },
        "/kontak": {
            "title": "Kontak Rumah Makan Padang Bateh Kota Bandung",
            "description": "Hubungi Rumah Makan Padang Bateh Kota untuk pesan nasi Padang, lauk, paket hemat, WhatsApp, dan GoFood atau ShopeeFood.",
        },
    }
    selected = page_seo.get(path, page_seo["/"])
    canonical = request.build_absolute_uri(request.path)
    schema = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "@id": canonical + "#restaurant",
        "name": restaurant.get("name", "RM Padang Bateh Kota"),
        "alternateName": ["Rumah Makan Bateh Kota", "RM Padang Bateh Kota Rajawali"],
        "url": request.build_absolute_uri("/"),
        "description": selected["description"],
        "image": [restaurant["logo"]] if restaurant.get("logo", "").startswith("http") else [],
        "servesCuisine": ["Masakan Padang", "Masakan Minang", "Indonesian"],
        "priceRange": "Rp5.000–Rp27.000",
        "telephone": "+" + restaurant.get("whatsapp", ""),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": restaurant.get("address", ""),
            "addressLocality": "Bandung",
            "addressRegion": "Jawa Barat",
            "addressCountry": "ID",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": restaurant.get("latitude"),
            "longitude": restaurant.get("longitude"),
        },
        "areaServed": ["Rajawali Barat", "Andir", "Bandung"],
        "hasMenu": request.build_absolute_uri("/menu/"),
        "sameAs": [url for url in [restaurant.get("gofood_url"), restaurant.get("shopee_url"), restaurant.get("instagram"), restaurant.get("facebook"), restaurant.get("tiktok")] if url],
    }
    if restaurant.get("rating") and restaurant.get("rating_count"):
        schema["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": restaurant["rating"], "ratingCount": restaurant["rating_count"]}
    day_map = {"Senin": "Monday", "Selasa": "Tuesday", "Rabu": "Wednesday", "Kamis": "Thursday", "Jumat": "Friday", "Sabtu": "Saturday", "Minggu": "Sunday"}
    schema["openingHoursSpecification"] = [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": f"https://schema.org/{day_map.get(hours.get('days'), hours.get('days'))}",
        "opens": hours.get("hours", "").split("–")[0].replace(".", ":"),
        "closes": hours.get("hours", "").split("–")[-1].replace(".", ":"),
    } for hours in restaurant.get("opening_hours", [])]
    seo = {**selected, "canonical": canonical, "schema_json": json.dumps(schema, ensure_ascii=False)}
    return {"restaurant": restaurant, "site_settings": service.settings(), "seo": seo}
