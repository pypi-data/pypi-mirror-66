import pycountry_un as wesp
import pycountry


class TestDb:
    def test_load_south_america(self):
        br = wesp.south_america.get(name="Brazil")
        print(type(br))
        assert br == pycountry.countries.get(name="Brazil")
