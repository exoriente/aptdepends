from aptmarkreason.shell.equivs import configure_control_file, create_empty_control_file, create_package_file


def test_configure_control_file():
    package_name ="test-package"
    test_file = create_empty_control_file(package_name)
    configure_control_file(test_file, package_name, ["dependency1", "dependency2", "dependency3"], "This is a test.")
    deb = create_package_file(test_file)
