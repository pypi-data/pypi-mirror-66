## @package officegenerator
## @brief Generate office files with predefined styles
from officegenerator.libodfgenerator import ODSStyleColor, ODSStyleCurrency, ColumnWidthODS, ODS_Read, ODS_Write, ODT, ODT_Standard, ODT_Manual_Styles, OdfCell, OdfSheet, guess_ods_style
from officegenerator.libxlsxgenerator import XLSX_Write, ColumnWidthXLSX
from officegenerator.commons import columnAdd, rowAdd, Coord, Range, __version__, __versiondate__
from officegenerator.objects.currency import Currency
from officegenerator.objects.percentage import Percentage
