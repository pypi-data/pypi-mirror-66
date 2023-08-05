import os
import wget
import pytest
from pvqa.utils.converters import pdf_converter

@pytest.fixture(scope="session")
def download_test_assets(tmpdir_factory):
    assets_urls = [
        # PDF
        "http://www.fao.org/3/a-i3278e.pdf",
        "https://www.nda.agric.za/docs/Brochures/ProdGuideCassava.pdf",
        "http://africasoilhealth.cabi.org/wpcms/wp-content/uploads/2015/04/126-CRAN-cassava-booklet.pdf",
    ]

    print("\nDownloading assets...")
    fn = tmpdir_factory.mktemp("assets_data")
    for url in assets_urls:
        wget.download(url=url, out=str(fn))
    return fn


class Test_converter:
    @pytest.fixture(autouse=True)
    def get_assets_folder(self, download_test_assets):
        self.assets_folder = download_test_assets

    def df_converter_check(self, df, include_line_breaks=False):
        errors = []
        # replace assertions by conditions
        if not df.shape == (3, 2):
            errors.append("resulting dataframe has unexpected shape.")
        if not (isinstance(df.paragraphs[0][0], str) and isinstance(df.title[0], str)):
            errors.append("paragraph column content has wrong format.")
        if include_line_breaks:
            para_len = [len(df.paragraphs[i]) for i in range(df.shape[0])]
            para_len.sort()
            if not para_len == [58, 80, 87]:
                errors.append(f"error in number of paragraphs : {para_len}")

        # assert no error message has been registered, else print messages
        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    def test_pdf_converter(self):
        df = pdf_converter(directory_path=self.assets_folder)
        self.df_converter_check(df)
        df_line_para = pdf_converter(
            directory_path=self.assets_folder, include_line_breaks=True
        )
        self.df_converter_check(df_line_para, True)