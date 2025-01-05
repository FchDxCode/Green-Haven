from django.test import TestCase
from django.core.cache import cache
from django.utils.text import slugify
from .services import GeminiService
from destinations.models import Destinations
from fauna.models import Fauna
from flora.models import Flora
from guides.models import Guides
from health.models import Health
from kuliner.models import Kuliner

class ChatbotTest(TestCase):
    def setUp(self):
        cache.clear()
        
        self.destination = Destinations.objects.create(
            title="Kebun Raya Bogor",
            description="Kebun raya tertua di Indonesia dengan koleksi tanaman yang beragam",
            location="Bogor, Jawa Barat",
            slug=slugify("Kebun Raya Bogor")
        )
        
        self.fauna = Fauna.objects.create(
            destinations=self.destination,
            title="Rusa Totol",
            description="Rusa yang hidup bebas di Kebun Raya Bogor",
            slug=slugify("Rusa Totol")
        )
        
        self.flora = Flora.objects.create(
            destinations=self.destination,
            title="Bunga Bangkai Raksasa",
            description="Bunga terbesar di dunia yang dapat ditemukan di Kebun Raya Bogor",
            slug=slugify("Bunga Bangkai Raksasa")
        )

        self.guide = Guides.objects.create(
            title="Panduan Wisata Bogor",
            description="Tips lengkap untuk wisata di Bogor",
            slug=slugify("Panduan Wisata Bogor")
        )

        self.health = Health.objects.create(
            destinations=self.destination,
            title="Klinik Wisata",
            description="Fasilitas kesehatan untuk wisatawan",
            slug=slugify("Klinik Wisata")
        )

        self.kuliner = Kuliner.objects.create(
            destinations=self.destination,
            title="Sate Kuningan",
            description="Kuliner khas Bogor",
            slug=slugify("Sate Kuningan")
        )
        
        self.gemini_service = GeminiService()

    def test_new_conversation(self):
        """Test first message in conversation"""
        response = self.gemini_service.get_response(
            "Apa saja destinasi wisata yang ada di Bogor?",
            "test_session_1"
        )
        
        self.assertTrue(response['text'].startswith("Hai! Saya Celya"))
        
        self.assertTrue(len(response['content_references']) > 0)
        
        self.assertTrue('bogor' in response['text'].lower())

    def test_follow_up_question(self):
        """Test conversation continuity"""
        self.gemini_service.get_response(
            "Ceritakan tentang Kebun Raya Bogor",
            "test_session_2"
        )
        
        response = self.gemini_service.get_response(
            "Dimana lokasinya?",
            "test_session_2"
        )
        
        self.assertFalse(response['text'].startswith("Hai! Saya Celya"))
        self.assertEqual(response['intent'], 'destination')
        self.assertTrue(any(ref['name'] == "Kebun Raya Bogor" 
                          for ref in response['content_references']))

    def test_unknown_topic(self):
        """Test response for unknown information"""
        response = self.gemini_service.get_response(
            "Ceritakan tentang Taman Nasional Kutai", 
            "test_session_3"
        )
        
        self.assertTrue('bogor' in response['text'].lower())
        
        self.assertEqual(len(response['content_references']), 0)
        
        helpful_response = any(
            phrase in response['text'].lower() for phrase in [
                'bisa',
                'rekomendasi',
                'wisata',
                'destinasi',
                'menarik'
            ]
        )
        self.assertTrue(helpful_response, 
                       "Response should contain helpful alternative suggestions")

    def test_content_references(self):
        """Test content references accuracy"""
        response = self.gemini_service.get_response(
            "Ada fauna apa saja di Kebun Raya Bogor?",  
            "test_session_4"
        )
        
        self.assertEqual(response['intent'], 'fauna')
        self.assertTrue(any(ref['name'] == "Rusa Totol" 
                          for ref in response['content_references']))

    def test_conversation_memory(self):
        """Test conversation context retention"""
        self.gemini_service.get_response(
            "Ceritakan tentang Kebun Raya Bogor",
            "test_session_5"
        )
        
        response = self.gemini_service.get_response(
            "Apa saja fauna yang ada di sana?",
            "test_session_5"
        )
        
        self.assertEqual(response['intent'], 'fauna')
        self.assertTrue(len(response['content_references']) > 0)

    def test_guide_info(self):
        """Test guide information"""
        response = self.gemini_service.get_response(
            "Ada panduan wisata apa saja untuk Bogor?",
            "test_session_6"
        )
        
        self.assertEqual(response['intent'], 'guide')
        self.assertTrue(any(ref['name'] == "Panduan Wisata Bogor" 
                          for ref in response['content_references']))

    def tearDown(self):
        cache.clear()
