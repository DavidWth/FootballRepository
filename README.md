Development in own environment: python -m venv venv
>  venv\Scripts\activate

Run tests
> in project root directory >   set PYTHONPATH=%PYTHONPATH%;%cd%\src
>   python -m unittest -v test.functional_tests.KickerFunctionalTest.test_get_club_controller
