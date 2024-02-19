python -m pytest test.py::TestTrendyol::test_fields_on_registration_page  -s
python -m pytest test.py::TestTrendyol::test_validation_error_on_empty_fields  -s
python -m pytest test.py::TestTrendyol::test_validation_error_on_blank_spaces  -s
python -m pytest test.py::TestTrendyol::test_add_to_cart  -s
python -m pytest test.py::TestTrendyol::test_add_to_wishlist  -s
python -m pytest test.py::TestTrendyol::test_logout -s