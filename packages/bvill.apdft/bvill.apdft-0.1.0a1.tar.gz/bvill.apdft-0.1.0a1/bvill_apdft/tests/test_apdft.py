import os
import PyPDF2
import io
from ..utils import flatten, get_pdfs_in_dir
from ..apdft import merge, write


def test_flatten():
    """Test the flatten function using a hardcoded list containing more lists"""

    print("Testing flatten function with deeply nested lists")
    test_deep_list = ["one", "two", ["three"], "four", ["five", "six", ["seven"]]]
    expected_result = ["one", "two", "three", "four", "five", "six", "seven"]
    assert flatten(test_deep_list) == expected_result

    print("Testing flatten function with list with no nested lists")
    test_shallow_list = ["one", "two", "three"]
    assert flatten(test_shallow_list) == test_shallow_list

    print("Testing flatten function with empty list")
    test_empty_list = []
    assert flatten(test_empty_list) == test_empty_list


def test_get_pdfs_in_dir():
    """Test the get_pdfs_in_dir function using the sample data folder in the repo"""

    print("Testing get_pdfs_in_dir function with sample data")
    test_dir = os.path.abspath("samples/dir")
    # this is the expected order to receive, notice non-pdf files missing
    rel_file_paths = [
        "samples/dir/4.pdf",
        "samples/dir/a/5.pdf",
        "samples/dir/0/6.pdf",
    ]
    # the result should contain all absolute file paths
    expected_result = [os.path.abspath(rel_file) for rel_file in rel_file_paths]
    assert get_pdfs_in_dir(test_dir) == expected_result

    print("Testing get_pdfs_in_dir function with same data but sorting turned off")
    test_dir = os.path.abspath("samples/dir")
    # this is the natural order received by os.listdir
    rel_file_paths = [
        "samples/dir/0/6.pdf",
        "samples/dir/4.pdf",
        "samples/dir/a/5.pdf",
    ]
    # the result should contain all absolute file paths
    expected_result = [os.path.abspath(rel_file) for rel_file in rel_file_paths]
    assert get_pdfs_in_dir(test_dir, disable_sorting=True) == expected_result


def test_merge():
    """
    Test the merge function using some of the sample data provided in the repo

    Todos:
        * Determine a better way to validate that PDF files have merged, e.g.
          by analyzing the merged file's metadata. New method will also need
          to verify that the files merged in the correct order
    """

    print("Testing merge function with a single file path")
    test_files = ["samples/sample2.pdf"]
    result_obj = merge(test_files)
    reader = PyPDF2.PdfFileReader(result_obj)
    assert reader.numPages == 1
    result_obj.close()

    print("Testing merge function with multiple file paths")
    test_files = ["samples/sample1.pdf", "samples/sample2.pdf", "samples/sample3.pdf"]
    result_obj = merge(test_files)
    reader = PyPDF2.PdfFileReader(result_obj)
    assert reader.numPages == 3
    result_obj.close()

    print("Testing the merge function with mix of files and directories")
    test_files = [
        "samples/sample2.pdf",
        "samples/more_pdfs",
        "samples/sample1.pdf",
    ]
    result_obj = merge(test_files)
    reader = PyPDF2.PdfFileReader(result_obj)
    assert reader.numPages == 5
    result_obj.close()

    print("Testing the merge function with a single directory")
    test_files = ["samples/more_pdfs"]
    result_obj = merge(test_files)
    reader = PyPDF2.PdfFileReader(result_obj)
    assert reader.numPages == 3
    result_obj.close()


def test_write():
    """Test the write function using some of the sample data provided in the repo"""
    print("Creating blank PDF file in memory")
    blank_pdf = PyPDF2.PdfFileWriter()
    blank_pdf.addBlankPage(width=float(612), height=(792))

    print(f"Creating test object from the blank PDF file")
    test_obj = io.BytesIO()
    blank_pdf.write(test_obj)

    test_write_file = "test_write.pdf"
    print(f"Writing test object to file {test_write_file}")
    # this should be None because we specified the resulting filename in the argument
    write_file_result = write(test_obj, test_write_file)
    assert write_file_result is None
    # check if the file exists
    assert os.path.exists(test_write_file)
    # clean up
    os.remove(test_write_file)

    print(f"Creating another test object from the blank PDF file")
    test_obj = io.BytesIO()
    blank_pdf.write(test_obj)

    test_write_dir = "test_write"
    print(f"Writing test object to directory {test_write_dir}")
    os.mkdir(test_write_dir)
    # this should be a timestamp-like filename with the '.pdf' extension
    write_dir_result = write(test_obj, test_write_dir)
    assert isinstance(write_dir_result, str)
    test_write_dir_result_path = os.path.join(test_write_dir, write_dir_result)
    # check if the file exists
    assert os.path.exists(test_write_dir_result_path)
    # clean up
    os.remove(test_write_dir_result_path)
    os.rmdir(test_write_dir)
