# License Notes

* Dean Wampler, October 24, 2025

This README describes my exploration of which licenses specified in the static datasets can be considered _permissive_.

> **NOTE:** Some, but not all of the JSON files written to disk from queries are also in the git repo.

## Loading License Datasets

Let's get some license datasets to use to analyze the licenses that appear in the Hugging Face metadata.

### ScanCode LicenseDB

First, I loaded a [JSON file of licenses](https://scancode-licensedb.aboutcode.org/index.json) from the [ScanCode LicenseDB](https://scancode-licensedb.aboutcode.org/) project to load into DuckDB, using the same `croissant.duckdb` database discussed in the [`README.md`](README.md) for the _static catalog_ project (this directory).

Next, I started the database and loaded the data:

```shell
duckdb croissant.duckdb
```

At the `D` prompt:

```sql
D CREATE OR REPLACE TABLE scancode_licenses AS
  SELECT *
  FROM read_json('scancode-licensedb.aboutcode.org.index.json');

D DESCRIBE scancode_licenses;
┌─────────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│       column_name       │ column_type │  null   │   key   │ default │  extra  │
│         varchar         │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ license_key             │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ category                │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_license_key        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ other_spdx_license_keys │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ is_exception            │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ is_deprecated           │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ json                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ yaml                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ html                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license                 │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
├─────────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 10 rows                                                             6 columns │
└───────────────────────────────────────────────────────────────────────────────┘
D SELECT count() FROM scancode_licenses;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│     2596     │
└──────────────┘
D SELECT * FROM scancode_licenses LIMIT 10;
┌──────────────────────┬──────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┐
│     license_key      │     category     │   spdx_license_key   │ … │         html         │       license        │
│       varchar        │     varchar      │       varchar        │   │       varchar        │       varchar        │
├──────────────────────┼──────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┤
│ 389-exception        │ Copyleft Limited │ 389-exception        │ … │ 389-exception.html   │ 389-exception.LICE…  │
│ 3com-microcode       │ Permissive       │ LicenseRef-scancod…  │ … │ 3com-microcode.html  │ 3com-microcode.LIC…  │
│ 3dslicer-1.0         │ Permissive       │ 3D-Slicer-1.0        │ … │ 3dslicer-1.0.html    │ 3dslicer-1.0.LICENSE │
│ 4suite-1.1           │ Permissive       │ LicenseRef-scancod…  │ … │ 4suite-1.1.html      │ 4suite-1.1.LICENSE   │
│ 996-icu-1.0          │ Free Restricted  │ LicenseRef-scancod…  │ … │ 996-icu-1.0.html     │ 996-icu-1.0.LICENSE  │
│ a-star-logic-memoi…  │ Proprietary Free │ LicenseRef-scancod…  │ … │ a-star-logic-memoi…  │ a-star-logic-memoi…  │
│ aardvark-py-2014     │ Proprietary Free │ LicenseRef-scancod…  │ … │ aardvark-py-2014.h…  │ aardvark-py-2014.L…  │
│ abrms                │ Proprietary Free │ LicenseRef-scancod…  │ … │ abrms.html           │ abrms.LICENSE        │
│ abstyles             │ Permissive       │ Abstyles             │ … │ abstyles.html        │ abstyles.LICENSE     │
│ ac3filter            │ Copyleft         │ LicenseRef-scancod…  │ … │ ac3filter.html       │ ac3filter.LICENSE    │
├──────────────────────┴──────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┤
│ 10 rows                                                                                     10 columns (5 shown) │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D
```

Notice there are **2596** licenses! We'll come back to this number...

What are the category values?

```sql
SELECT DISTINCT category
FROM scan_licenses;

┌──────────────────┐
│     category     │
│     varchar      │
├──────────────────┤
│ Commercial       │
│ CLA              │
│ Unstated License │
│ Patent License   │
│ Proprietary Free │
│ Copyleft         │
│ Copyleft Limited │
│ Source-available │
│ Permissive       │
│ Public Domain    │
│ Free Restricted  │
├──────────────────┤
│     11 rows      │
└──────────────────┘
```

Here's what we can say about these catagories for our purposes:

| Category           | Comment |
| :----------------- | :------ |
| `Commercial`       | Not open, so not suitable. |
| `CLA`              | Usually associated with restrictive licensing. |
| `Unstated License` | Not usable |
| `Patent License`.  | Same |
| `Proprietary Free` | Not usable by us currently, because of restrictions, but it's possible that we will support these in the future. |
| `Copyleft`         | GNU and not sufficiently permissive. Also less appropriate for data vs. code. |
| `Copyleft Limited` | Same |
| `Source-available` | Not appropriate for data. Designed for code. |
| `Permissive`       | Acceptable |
| `Public Domain`    | Acceptable |
| `Free Restricted`  | Similar to `Proprietary Free`, but more open. Still, we are not supporting these datasets at this time. |

Hence, the only two we want to use at this time are `Permissive` and `Public Domain`. 

### SPDX License Data

Similarly, I downloaded a [JSON file `licenses.json`](https://github.com/spdx/license-list-data/blob/main/json/licenses.json) of [SPDX licenses](https://spdx.org/licenses/). However, I needed to extract the list of licenses from it before loading into duckdb. I used [`jq`](https://jqlang.org/).

```shell
jq '.licenses' licenses.json >spdx-licenses.json
```

Now create the table:

```sql
D CREATE OR REPLACE TABLE spdx_licenses AS
  SELECT *
  FROM read_json('spdx-licenses.json');

D DESCRIBE spdx_licenses;
┌───────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│      column_name      │ column_type │  null   │   key   │ default │  extra  │
│        varchar        │   varchar   │ varchar │ varchar │ varchar │ varchar │
├───────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ reference             │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ isDeprecatedLicenseId │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ detailsUrl            │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ referenceNumber       │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ name                  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ licenseId             │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ seeAlso               │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ isOsiApproved         │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ isFsfLibre            │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT count() FROM spdx_licenses;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│     710      │
└──────────────┘
D SELECT * FROM spdx_licenses LIMIT 10;
┌──────────────────────┬──────────────────────┬───┬──────────────────────┬───────────────┬────────────┐
│      reference       │ isDeprecatedLicens…  │ … │       seeAlso        │ isOsiApproved │ isFsfLibre │
│       varchar        │       boolean        │   │      varchar[]       │    boolean    │  boolean   │
├──────────────────────┼──────────────────────┼───┼──────────────────────┼───────────────┼────────────┤
│ https://spdx.org/l…  │ false                │ … │ ['http://landley.n…  │ true          │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://slicer.o…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://opensour…  │ true          │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://fedorapr…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://github.c…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://fedorapr…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://gitlab.f…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://fedorapr…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://gitlab.f…  │ false         │ NULL       │
│ https://spdx.org/l…  │ false                │ … │ ['https://fedorapr…  │ false         │ NULL       │
├──────────────────────┴──────────────────────┴───┴──────────────────────┴───────────────┴────────────┤
│ 10 rows                                                                         9 columns (5 shown) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This set is smaller: **710**.

Let's combine these two tables. `spdx_licenses.licenseId` is (or should be!) equivalent to `scancode_licenses.spdx_license_key` so we join on those columns.

```sql
D CREATE OR REPLACE TABLE spdx_scancode_licenses AS
SELECT
  spdx.licenseId AS spdx_licenseId,
  scan.spdx_license_key AS scan_spdx_license_key,
  scan.license_key AS scan_license_key,
  scan.license AS scan_license,
  spdx.name AS spdx_name,
  scan.category AS scan_category,
  scan.other_spdx_license_keys AS scan_other_spdx_license_keys,
  scan.is_exception AS scan_is_exception,
  scan.is_deprecated AS scan_is_deprecated,
  scan.json AS scan_json,
  scan.yaml AS scan_yaml,
  scan.html AS scan_html,
  spdx.reference AS spdx_reference,
  spdx.isDeprecatedLicenseId AS spdx_isDeprecatedLicenseId,
  spdx.detailsUrl AS spdx_detailsUrl,
  spdx.referenceNumber AS spdx_referenceNumber,
  spdx.seeAlso AS spdx_seeAlso,
  spdx.isOsiApproved AS spdx_isOsiApproved,
  spdx.isFsfLibre AS spdx_isFsfLibre
FROM spdx_licenses AS spdx
JOIN scancode_licenses AS scan
  ON spdx.licenseId = scan.spdx_license_key;

D DESCRIBE spdx_scancode_licenses;
┌──────────────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│         column_name          │ column_type │  null   │   key   │ default │  extra  │
│           varchar            │   varchar   │ varchar │ varchar │ varchar │ varchar │
├──────────────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ spdx_licenseId               │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_spdx_license_key        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_license_key             │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_license                 │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_name                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_category                │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_other_spdx_license_keys │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_is_exception            │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_is_deprecated           │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_json                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_yaml                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ scan_html                    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_reference               │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_isDeprecatedLicenseId   │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_detailsUrl              │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_referenceNumber         │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_seeAlso                 │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_isOsiApproved           │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
│ spdx_isFsfLibre              │ BOOLEAN     │ YES     │ NULL    │ NULL    │ NULL    │
├──────────────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 19 rows                                                                  6 columns │
└────────────────────────────────────────────────────────────────────────────────────┘
D SELECT count() FROM spdx_scancode_licenses;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│     675      │
└──────────────┘
D SELECT * FROM spdx_scancode_licenses LIMIT 10;
┌────────────────┬──────────────────────┬───┬──────────────────────┬────────────────────┬─────────────────┐
│ spdx_licenseId │ scan_spdx_license_…  │ … │     spdx_seeAlso     │ spdx_isOsiApproved │ spdx_isFsfLibre │
│    varchar     │       varchar        │   │      varchar[]       │      boolean       │     boolean     │
├────────────────┼──────────────────────┼───┼──────────────────────┼────────────────────┼─────────────────┤
│ 3D-Slicer-1.0  │ 3D-Slicer-1.0        │ … │ ['https://slicer.o…  │ false              │ NULL            │
│ Abstyles       │ Abstyles             │ … │ ['https://fedorapr…  │ false              │ NULL            │
│ CDL-1.0        │ CDL-1.0              │ … │ ['http://www.opens…  │ false              │ NULL            │
│ DOC            │ DOC                  │ … │ ['http://www.cs.wu…  │ false              │ NULL            │
│ AdaCore-doc    │ AdaCore-doc          │ … │ ['https://github.c…  │ false              │ NULL            │
│ APL-1.0        │ APL-1.0              │ … │ ['https://opensour…  │ true               │ NULL            │
│ Adobe-Glyph    │ Adobe-Glyph          │ … │ ['https://fedorapr…  │ false              │ NULL            │
│ Adobe-2006     │ Adobe-2006           │ … │ ['https://fedorapr…  │ false              │ NULL            │
│ Adobe-Utopia   │ Adobe-Utopia         │ … │ ['https://gitlab.f…  │ false              │ NULL            │
│ ADSL           │ ADSL                 │ … │ ['https://fedorapr…  │ false              │ NULL            │
├────────────────┴──────────────────────┴───┴──────────────────────┴────────────────────┴─────────────────┤
│ 10 rows                                                                            19 columns (5 shown) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

At most, we could expect **710** rows, but we get **675**, suggesting some of licenses are not in both tables.

```sql
SELECT
  spdx.licenseId AS spdx_licenseId,
  scan.spdx_license_key AS scan_spdx_license_key,
  scan.license_key AS scan_license_key,
  scan.license AS scan_license,
  spdx.name AS spdx_name,
  scan.category AS scan_category,
FROM spdx_licenses AS spdx
LEFT OUTER JOIN scancode_licenses AS scan
  ON spdx.licenseId = scan.spdx_license_key
WHERE scan.spdx_license_key IS NULL;

┌──────────────────────┬──────────────────────┬──────────────────┬──────────────┬─────────────────────────┬───────────────┐
│    spdx_licenseId    │ scan_spdx_license_…  │ scan_license_key │ scan_license │        spdx_name        │ scan_category │
│       varchar        │       varchar        │     varchar      │   varchar    │         varchar         │    varchar    │
├──────────────────────┼──────────────────────┼──────────────────┼──────────────┼─────────────────────────┼───────────────┤
│ AGPL-1.0             │ NULL                 │ NULL             │ NULL         │ Affero General Public…  │ NULL          │
│ ESA-PL-strong-copy…  │ NULL                 │ NULL             │ NULL         │ European Space Agency…  │ NULL          │
│ OSSP                 │ NULL                 │ NULL             │ NULL         │ OSSP License            │ NULL          │
│ GPL-1.0              │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ ESA-PL-permissive-…  │ NULL                 │ NULL             │ NULL         │ European Space Agency…  │ NULL          │
│ ESA-PL-weak-copyle…  │ NULL                 │ NULL             │ NULL         │ European Space Agency…  │ NULL          │
│ LGPL-2.1+            │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Pu…  │ NULL          │
│ Net-SNMP             │ NULL                 │ NULL             │ NULL         │ Net-SNMP License        │ NULL          │
│ StandardML-NJ        │ NULL                 │ NULL             │ NULL         │ Standard ML of New Je…  │ NULL          │
│ Advanced-Cryptics-…  │ NULL                 │ NULL             │ NULL         │ Advanced Cryptics Dic…  │ NULL          │
│ BSD-Mark-Modificat…  │ NULL                 │ NULL             │ NULL         │ BSD Mark Modification…  │ NULL          │
│ HPND-SMC             │ NULL                 │ NULL             │ NULL         │ Historical Permission…  │ NULL          │
│ GFDL-1.2             │ NULL                 │ NULL             │ NULL         │ GNU Free Documentatio…  │ NULL          │
│ GFDL-1.1             │ NULL                 │ NULL             │ NULL         │ GNU Free Documentatio…  │ NULL          │
│ GPL-3.0+             │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ SGMLUG-PM            │ NULL                 │ NULL             │ NULL         │ SGMLUG Parser Materia…  │ NULL          │
│ LGPL-2.1             │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Pu…  │ NULL          │
│ LGPL-3.0             │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Pu…  │ NULL          │
│ WTFNMFPL             │ NULL                 │ NULL             │ NULL         │ Do What The F*ck You …  │ NULL          │
│ BSD-2-Clause-NetBSD  │ NULL                 │ NULL             │ NULL         │ BSD 2-Clause NetBSD L…  │ NULL          │
│ GFDL-1.3             │ NULL                 │ NULL             │ NULL         │ GNU Free Documentatio…  │ NULL          │
│ GPL-2.0              │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ LGPL-3.0+            │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Pu…  │ NULL          │
│ GPL-2.0-with-bison…  │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ WordNet              │ NULL                 │ NULL             │ NULL         │ WordNet License         │ NULL          │
│ BSD-3-Clause-Tso     │ NULL                 │ NULL             │ NULL         │ BSD 3-Clause Tso vari…  │ NULL          │
│ bzip2-1.0.5          │ NULL                 │ NULL             │ NULL         │ bzip2 and libbzip2 Li…  │ NULL          │
│ GPL-2.0+             │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ LGPL-2.0+            │ NULL                 │ NULL             │ NULL         │ GNU Library General P…  │ NULL          │
│ GPL-3.0              │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ AGPL-3.0             │ NULL                 │ NULL             │ NULL         │ GNU Affero General Pu…  │ NULL          │
│ LGPL-2.0             │ NULL                 │ NULL             │ NULL         │ GNU Library General P…  │ NULL          │
│ BSD-2-Clause-FreeBSD │ NULL                 │ NULL             │ NULL         │ BSD 2-Clause FreeBSD …  │ NULL          │
│ GPL-1.0+             │ NULL                 │ NULL             │ NULL         │ GNU General Public Li…  │ NULL          │
│ Nunit                │ NULL                 │ NULL             │ NULL         │ Nunit License           │ NULL          │
├──────────────────────┴──────────────────────┴──────────────────┴──────────────┴─────────────────────────┴───────────────┤
│ 35 rows                                                                                                       6 columns │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Most, but not all are GPL variants. Previously, we saw that we want to keep only licenses that the ScanCode dataset categories as `Permissive` or `Public Domain`. _We can't use that criterium here, because those 35 rows all appeared in the SPDX data, but not the ScanCode data._ However, the SPDX data includes a column `isOsiApproved`. Let's use that:

```sql
SELECT
  spdx.licenseId AS spdx_licenseId,
  scan.spdx_license_key AS scan_spdx_license_key,
  scan.license_key AS scan_license_key,
  scan.license AS scan_license,
  spdx.name AS spdx_name,
  scan.category AS scan_category,
FROM spdx_licenses AS spdx
LEFT OUTER JOIN scancode_licenses AS scan
  ON spdx.licenseId = scan.spdx_license_key
WHERE scan.spdx_license_key IS NULL
 AND  spdx.isOsiApproved IS TRUE;

┌────────────────┬──────────────────────┬──────────────────┬──────────────┬───────────────────────────────┬───────────────┐
│ spdx_licenseId │ scan_spdx_license_…  │ scan_license_key │ scan_license │           spdx_name           │ scan_category │
│    varchar     │       varchar        │     varchar      │   varchar    │            varchar            │    varchar    │
├────────────────┼──────────────────────┼──────────────────┼──────────────┼───────────────────────────────┼───────────────┤
│ LGPL-2.1+      │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Public L…  │ NULL          │
│ GPL-3.0+       │ NULL                 │ NULL             │ NULL         │ GNU General Public License …  │ NULL          │
│ LGPL-2.1       │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Public L…  │ NULL          │
│ LGPL-3.0       │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Public L…  │ NULL          │
│ GPL-2.0        │ NULL                 │ NULL             │ NULL         │ GNU General Public License …  │ NULL          │
│ LGPL-3.0+      │ NULL                 │ NULL             │ NULL         │ GNU Lesser General Public L…  │ NULL          │
│ WordNet        │ NULL                 │ NULL             │ NULL         │ WordNet License               │ NULL          │
│ GPL-2.0+       │ NULL                 │ NULL             │ NULL         │ GNU General Public License …  │ NULL          │
│ LGPL-2.0+      │ NULL                 │ NULL             │ NULL         │ GNU Library General Public …  │ NULL          │
│ GPL-3.0        │ NULL                 │ NULL             │ NULL         │ GNU General Public License …  │ NULL          │
│ AGPL-3.0       │ NULL                 │ NULL             │ NULL         │ GNU Affero General Public L…  │ NULL          │
│ LGPL-2.0       │ NULL                 │ NULL             │ NULL         │ GNU Library General Public …  │ NULL          │
├────────────────┴──────────────────────┴──────────────────┴──────────────┴───────────────────────────────┴───────────────┤
│ 12 rows                                                                                                       6 columns │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Note that for GPL licenses, `isOsiApproved` is `TRUE`, but we don't want consider those licenses suitable for our needs. We'll ignore the obscure WordNet license. 

Hence, the 675-row `spdx_scancode_licenses` table is all we'll need.

## What Licenses Are in the HF Metadata?

We discovered when creating the static catalog that many datasets specify a license, but not in a valid form, i.e., a non-existent choosealicense.com URL is used. To determine those cases, let's first confirm that when an invalid URL is used, the `license_id` and `license` are both `NULL`. We'll use the `hf_metadata_with_bad_licenses` table described in the README's [Invalid Licenses](README.md#invalid-licenses) section.

```sql
SELECT license_id, license, license_url
FROM hf_metadata_with_bad_licenses
WHERE license_url NOT NULL AND ( license_id IS NULL OR license IS NULL );

SELECT license_id, license, license_url
FROM hf_metadata_with_bad_licenses
WHERE license_url NOT NULL AND license_id IS NULL AND license IS NULL;
```

Both queries return 17610 rows! Since the second query also returns the same rows, it demonstrates that if one of `license` or `license_id` is `NULL`, then both are `NULL`.

Let's confirm that the URL is never `NULL` if either `license` or `license_id` is not `NULL`:

```sql
SELECT license_id, license, license_url
FROM hf_metadata_with_bad_licenses
WHERE license_url IS NULL AND ( license NOT NULL OR license_url NOT NULL );
```

This returns zero rows. 

Hence, we can examine the incorrectly specified licenses by looking only at the URLs. Let's find the unique values:

```sql
SELECT license_url, count() AS count
FROM (
  SELECT license_url
  FROM   hf_metadata_with_bad_licenses
  WHERE  license_url NOT NULL AND license_id IS NULL AND license IS NULL)
GROUP BY license_url
ORDER BY count DESC;
┌──────────────────────────────────────────────────────────────────────────┬───────┐
│                               license_url                                │ count │
│                                 varchar                                  │ int64 │
├──────────────────────────────────────────────────────────────────────────┼───────┤
│ https://choosealicense.com/licenses/openrail/                            │  4654 │
│ https://choosealicense.com/licenses/unknown/                             │  2271 │
│ https://choosealicense.com/licenses/other/                               │  1718 │
│ https://choosealicense.com/licenses/cc-by-nc-4.0/                        │  1693 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-4.0/                     │  1410 │
│ https://choosealicense.com/licenses/cc/                                  │   947 │
│ https://choosealicense.com/licenses/odc-by/                              │   618 │
│ https://choosealicense.com/licenses/cc-by-nc-nd-4.0/                     │   549 │
│ https://choosealicense.com/licenses/cc-by-sa-3.0/                        │   492 │
│ https://choosealicense.com/licenses/gpl/                                 │   427 │
│ https://choosealicense.com/licenses/creativeml-openrail-m/               │   320 │
│ https://choosealicense.com/licenses/odbl/                                │   298 │
│ https://choosealicense.com/licenses/llama2/                              │   212 │
│ https://choosealicense.com/licenses/llama3/                              │   186 │
│ https://choosealicense.com/licenses/cc-by-3.0/                           │   179 │
│ https://choosealicense.com/licenses/cc-by-2.0/                           │   163 │
│ https://choosealicense.com/licenses/llama3.1/                            │   161 │
│ https://choosealicense.com/licenses/bsd/                                 │   137 │
│ https://choosealicense.com/licenses/cc-by-nd-4.0/                        │   118 │
│ https://choosealicense.com/licenses/llama3.2/                            │   104 │
│                       ·                                                  │     · │
│                       ·                                                  │     · │
│                       ·                                                  │     · │
│ https://choosealicense.com/licenses/bigscience-openrail-m/               │    58 │
│ https://choosealicense.com/licenses/cdla-sharing-1.0/                    │    57 │
│ https://choosealicense.com/licenses/openrail++/                          │    55 │
│ https://choosealicense.com/licenses/llama3.3/                            │    41 │
│ https://choosealicense.com/licenses/gemma/                               │    33 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-2.0/                     │    31 │
│ https://choosealicense.com/licenses/cc-by-nc-nd-3.0/                     │    25 │
│ https://choosealicense.com/licenses/bigcode-openrail-m/                  │    25 │
│ https://choosealicense.com/licenses/gfdl/                                │    23 │
│ https://choosealicense.com/licenses/etalab-2.0/                          │    21 │
│ https://choosealicense.com/licenses/cc-by-2.5/                           │    21 │
│ https://choosealicense.com/licenses/bigscience-bloom-rail-1.0/           │    15 │
│ https://choosealicense.com/licenses/cdla-permissive-1.0/                 │    10 │
│ https://choosealicense.com/licenses/lgpl/                                │     6 │
│ https://choosealicense.com/licenses/apple-amlr/                          │     4 │
│ https://choosealicense.com/licenses/llama4/                              │     4 │
│ https://choosealicense.com/licenses/lgpl-lr/                             │     2 │
│ https://choosealicense.com/licenses/deepfloyd-if-license/                │     1 │
│ https://choosealicense.com/licenses/fair-noncommercial-research-license/ │     1 │
│ https://choosealicense.com/licenses/intel-research/                      │     1 │
├──────────────────────────────────────────────────────────────────────────┴───────┤
│ 47 rows (40 shown)                                                     2 columns │
└──────────────────────────────────────────────────────────────────────────────────┘
```

The URLs are of the form, `https://choosealicense.com/licenses/cc-by-nc-sa-4.0/`, where the last part looks like an identifier. Lets use duckdb's `regex` function to extract that part.

```sql
SELECT DISTINCT rtrim(regexp_replace(license_url, 'https://choosealicense.com/licenses/', ''), '/') AS id
FROM hf_metadata_with_bad_licenses 
WHERE license_url NOT NULL AND license_id IS NULL AND license IS NULL;
```

This returns 47 rows, but we can drop six values: `gpl`, `lgpl`, `lgpl-lr`, `other`, `undefined`, and `unknown`. Doing that, we create a new table `bad_licenses`, and write the values to a file:

```sql
CREATE OR REPLACE TABLE bad_licenses AS
SELECT id, count() AS count
FROM (
  SELECT 
  CASE WHEN id = 'gpl'       THEN NULL
       WHEN id = 'lgpl'      THEN NULL
       WHEN id = 'lgpl-lr'   THEN NULL
       WHEN id = 'other'     THEN NULL
       WHEN id = 'undefined' THEN NULL
       WHEN id = 'unknown'   THEN NULL
       ELSE id
       END AS id
  FROM (
    SELECT rtrim(regexp_replace(license_url, 'https://choosealicense.com/licenses/', ''), '/') AS id
    FROM hf_metadata_with_bad_licenses
    WHERE license_url NOT NULL AND license_id IS NULL AND license IS NULL
  )
)
WHERE id NOT NULL
GROUP BY id
ORDER BY count DESC;

COPY bad_licenses TO 'bad-licenses.json';
SELECT count() FROM bad_licenses;
```

This table has 41 rows. We could ignore the low-usage licenses, but we'll plow ahead for now as if all are equally important...

Some of the values we see include familiar categories like `cc-by-*`, `cdla-*`, `gemma*`, `llama*`, `bigcode*`, `bigscience*`, etc. Let's now join `bad_licenses` with `spdx_scancode_licenses` to see which of these are considered permissive.

Let's use the larger `scancode_licenses` table to find out which of these 41 values might match real licenses and see how they are categorized:

```sql
SELECT license_key, spdx_license_key, category, count
FROM scancode_licenses
JOIN (
  SELECT id, count
  FROM bad_licenses
) AS bad
ON bad.id = license_key
ORDER BY bad.id ASC;
┌─────────────────────┬─────────────────────┬──────────────────┬───────┐
│     license_key     │  spdx_license_key   │     category     │ count │
│       varchar       │       varchar       │     varchar      │ int64 │
├─────────────────────┼─────────────────────┼──────────────────┼───────┤
│ cc-by-2.0           │ CC-BY-2.0           │ Permissive       │   163 │
│ cc-by-2.5           │ CC-BY-2.5           │ Permissive       │    21 │
│ cc-by-3.0           │ CC-BY-3.0           │ Permissive       │   179 │
│ cc-by-nc-2.0        │ CC-BY-NC-2.0        │ Source-available │    81 │
│ cc-by-nc-3.0        │ CC-BY-NC-3.0        │ Source-available │    61 │
│ cc-by-nc-4.0        │ CC-BY-NC-4.0        │ Source-available │  1693 │
│ cc-by-nc-nd-3.0     │ CC-BY-NC-ND-3.0     │ Source-available │    25 │
│ cc-by-nc-nd-4.0     │ CC-BY-NC-ND-4.0     │ Source-available │   549 │
│ cc-by-nc-sa-2.0     │ CC-BY-NC-SA-2.0     │ Source-available │    31 │
│ cc-by-nc-sa-3.0     │ CC-BY-NC-SA-3.0     │ Source-available │    68 │
│ cc-by-nc-sa-4.0     │ CC-BY-NC-SA-4.0     │ Source-available │  1410 │
│ cc-by-nd-4.0        │ CC-BY-ND-4.0        │ Source-available │   118 │
│ cc-by-sa-3.0        │ CC-BY-SA-3.0        │ Copyleft Limited │   492 │
│ cdla-permissive-1.0 │ CDLA-Permissive-1.0 │ Permissive       │    10 │
│ cdla-permissive-2.0 │ CDLA-Permissive-2.0 │ Permissive       │    80 │
│ cdla-sharing-1.0    │ CDLA-Sharing-1.0    │ Copyleft Limited │    57 │
│ etalab-2.0          │ etalab-2.0          │ Permissive       │    21 │
├─────────────────────┴─────────────────────┴──────────────────┴───────┤
│ 17 rows                                                    4 columns │
└──────────────────────────────────────────────────────────────────────┘
```

So, of these 17, the permissive licenses are:

* `cc-by-2.0`
* `cc-by-2.5`
* `cc-by-3.0`
* `cdla-permissive-1.0`
* `cdla-permissive-2.0`
* `etalab-2.0`

> **NOTE:** Even thought CDLA is supposed to be an ideal data license, it is not used very much!

Let's look more carefully at the other cases that didn't match. There might be substrings we can use. Let's try substring matching for all cases.

```sql
SELECT license_key, category
FROM   scancode_licenses
WHERE  license_key LIKE '%llama%';

┌────────────────────────┬──────────────────┐
│      license_key       │     category     │
│        varchar         │     varchar      │
├────────────────────────┼──────────────────┤
│ llama-2-license-2023   │ Proprietary Free │
│ llama-3.1-license-2024 │ Proprietary Free │
│ llama-3.2-license-2024 │ Proprietary Free │
│ llama-3.3-license-2024 │ Proprietary Free │
│ llama-4-cla-2025       │ Proprietary Free │
│ llama-4-license-2025   │ Proprietary Free │
│ llama-license-2023     │ Proprietary Free │
└────────────────────────┴──────────────────┘
```

None of the `llama` models can be used by us currently. They are designed primarily for Llama models anyway, rather than data.

How about `bigcode` and `bigscience`?

```sql
SELECT license_key, category
  FROM scancode_licenses
  WHERE license_key LIKE '%big%';
┌─────────────────────────┬──────────────────┐
│       license_key       │     category     │
│         varchar         │     varchar      │
├─────────────────────────┼──────────────────┤
│ bigcode-open-rail-m-v1  │ Proprietary Free │
│ bigdigits               │ Permissive       │
│ bigelow-holmes          │ Permissive       │
│ bigscience-open-rail-m  │ Proprietary Free │
│ bigscience-open-rail-m2 │ Proprietary Free │
│ bigscience-rail-1.0     │ Proprietary Free │
│ morbig-ieee-std-usage   │ Permissive       │
└─────────────────────────┴──────────────────┘
```

In fact, those licenses are known to be restrictive, based on their source datasets.

It turns that query also finds all the `rail` licenses, too.

And more of the "bad" licenses...

```sql
SELECT license_key, category
  FROM scancode_licenses
  WHERE license_key LIKE '%odc%';
┌─────────────┬────────────┐
│ license_key │  category  │
│   varchar   │  varchar   │
├─────────────┼────────────┤
│ odc-1.0     │ Copyleft   │
│ odc-by-1.0  │ Permissive │
└─────────────┴────────────┘
```

```sql
SELECT license_key, category
  FROM scancode_licenses
  WHERE license_key LIKE '%odbl%';
┌─────────────┬──────────┐
│ license_key │ category │
│   varchar   │ varchar  │
├─────────────┼──────────┤
│ odbl-1.0    │ Copyleft │
└─────────────┴──────────┘
```

```sql
SELECT license_key, category
  FROM scancode_licenses
  WHERE license_key LIKE '%pddl%';
┌─────────────┬───────────────┐
│ license_key │   category    │
│   varchar   │    varchar    │
├─────────────┼───────────────┤
│ pddl-1.0    │ Public Domain │
└─────────────┴───────────────┘
```

```sql
SELECT license_key, category
  FROM scancode_licenses
  WHERE license_key LIKE '%fair%';
┌───────────────────────┬──────────────────┐
│      license_key      │     category     │
│        varchar        │     varchar      │
├───────────────────────┼──────────────────┤
│ broadleaf-fair-use    │ Proprietary Free │
│ fair                  │ Permissive       │
│ fair-ai-public-1.0    │ Copyleft         │
│ fair-ai-public-1.0-sd │ Proprietary Free │
│ fair-source-0.9       │ Source-available │
└───────────────────────┴──────────────────┘
```

```sql
SELECT license_key, category
    FROM scancode_licenses
    WHERE license_key LIKE '%apple%';
┌─────────────────────────────────┬──────────────────┐
│           license_key           │     category     │
│             varchar             │     varchar      │
├─────────────────────────────────┼──────────────────┤
│ apple-academic-lisa-os-3.1      │ Proprietary Free │
│ apple-attribution               │ Permissive       │
│ apple-attribution-1997          │ Permissive       │
│ apple-excl                      │ Permissive       │
│ apple-mfi-license               │ Proprietary Free │
│ apple-ml-ferret-2023            │ Permissive       │
│ apple-mpeg-4                    │ Free Restricted  │
│ apple-runtime-library-exception │ Permissive       │
│ apple-sscl                      │ Permissive       │
│ cups-apple-os-exception         │ Copyleft Limited │
│ egrappler                       │ Commercial       │
├─────────────────────────────────┴──────────────────┤
│ 11 rows                                  2 columns │
└────────────────────────────────────────────────────┘
```

For `bsd` and `cc`, `WHERE license_key LIKE '%bsd'`, etc. returns a lot of licenses, so it helps to add to the clause: 

```sql
SELECT license_key, category
    FROM scancode_licenses
    WHERE license_key LIKE '%cc%' AND category LIKE 'P%';
┌─────────────────────────────────────────┬──────────────────┐
│               license_key               │     category     │
│                 varchar                 │     varchar      │
├─────────────────────────────────────────┼──────────────────┤
│ accellera-systemc                       │ Permissive       │
│ cc-by-1.0                               │ Permissive       │
│ cc-by-2.0                               │ Permissive       │
│ cc-by-2.0-uk                            │ Permissive       │
│ cc-by-2.5                               │ Permissive       │
│ cc-by-2.5-au                            │ Permissive       │
│ cc-by-3.0                               │ Permissive       │
│ cc-by-3.0-at                            │ Permissive       │
│ cc-by-3.0-au                            │ Permissive       │
│ cc-by-3.0-de                            │ Permissive       │
│ cc-by-3.0-igo                           │ Permissive       │
│ cc-by-3.0-nl                            │ Permissive       │
│ cc-by-3.0-us                            │ Permissive       │
│ cc-by-4.0                               │ Permissive       │
│ cc-devnations-2.0                       │ Proprietary Free │
│ cc-nc-sampling-plus-1.0                 │ Proprietary Free │
│ cc-pd                                   │ Public Domain    │
│ cc-pdm-1.0                              │ Public Domain    │
│ cc-sampling-1.0                         │ Proprietary Free │
│ cc-sampling-plus-1.0                    │ Proprietary Free │
│ cc0-1.0                                 │ Public Domain    │
│ ccg-research-academic                   │ Proprietary Free │
│ corporate-accountability-1.1            │ Proprietary Free │
│ corporate-accountability-commercial-1.1 │ Proprietary Free │
│ gareth-mccaughan                        │ Permissive       │
│ nvidia-nccl-sla-2016                    │ Proprietary Free │
│ sun-cc-pp-1.0                           │ Proprietary Free │
├─────────────────────────────────────────┴──────────────────┤
│ 27 rows                                          2 columns │
└────────────────────────────────────────────────────────────┘
```

There are _93_ BSD licenses, 80 of which are `Permissive`.

```sql
SELECT category, count() AS count
FROM   scancode_licenses
WHERE  license_key LIKE '%bsd%'
GROUP BY category
ORDER BY count DESC;
┌──────────────────┬───────┐
│     category     │ count │
│     varchar      │ int64 │
├──────────────────┼───────┤
│ Permissive       │    80 │
│ Free Restricted  │     8 │
│ Copyleft Limited │     2 │
│ Proprietary Free │     2 │
│ Copyleft         │     1 │
└──────────────────┴───────┘
```

We list the permissive ones in the next section.

## Other Permissive Licenses

To summarize, the following are the other `Permissive` or `Public Domain` licenses that are similar to the "bad" licenses we found, which _may_ match improperly specified licenses in the data sets. We also summarize how we identified them. The `count` is only shown for the exact matches we saw above:

| License Key                              | How Matched      | Count |
| :--------------------------------------- | :--------------- | ----: |
| `accellera-systemc`                      | `LIKE '%cc%'`    |       |
| `adi-bsd`                                | `LIKE '%bsd%'`   |       |
| `agere-bsd`                              | `LIKE '%bsd%'`   |       |
| `apple-attribution-1997`                 | `LIKE '%apple%'` |       |
| `apple-attribution`                      | `LIKE '%apple%'` |       |
| `apple-excl`                             | `LIKE '%apple%'` |       |
| `apple-ml-ferret-2023`                   | `LIKE '%apple%'` |       |
| `apple-runtime-library-exception`        | `LIKE '%apple%'` |       |
| `apple-sscl`                             | `LIKE '%apple%'` |       |
| `bigdigits`                              | `LIKE '%big%'`   |       |
| `bigelow-holmes`                         | `LIKE '%big%'`   |       |
| `bsd-1-clause`                           | `LIKE '%bsd%'`   |       |
| `bsd-1-clause-build`                     | `LIKE '%bsd%'`   |       |
| `bsd-1988`                               | `LIKE '%bsd%'`   |       |
| `bsd-2-clause-first-lines`               | `LIKE '%bsd%'`   |       |
| `bsd-2-clause-freebsd`                   | `LIKE '%bsd%'`   |       |
| `bsd-2-clause-netbsd`                    | `LIKE '%bsd%'`   |       |
| `bsd-2-clause-pkgconf-disclaimer`        | `LIKE '%bsd%'`   |       |
| `bsd-2-clause-plus-advertizing`          | `LIKE '%bsd%'`   |       |
| `bsd-2-clause-views`                     | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-devine`                    | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-fda`                       | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-hp`                        | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-jtag`                      | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-no-change`                 | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-no-trademark`              | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-open-mpi`                  | `LIKE '%bsd%'`   |       |
| `bsd-3-clause-sun`                       | `LIKE '%bsd%'`   |       |
| `bsd-4-clause-shortened`                 | `LIKE '%bsd%'`   |       |
| `bsd-ack`                                | `LIKE '%bsd%'`   |       |
| `bsd-ack-carrot2`                        | `LIKE '%bsd%'`   |       |
| `bsd-advertising-acknowledgement`        | `LIKE '%bsd%'`   |       |
| `bsd-artwork`                            | `LIKE '%bsd%'`   |       |
| `bsd-atmel`                              | `LIKE '%bsd%'`   |       |
| `bsd-axis-nomod`                         | `LIKE '%bsd%'`   |       |
| `bsd-axis`                               | `LIKE '%bsd%'`   |       |
| `bsd-credit`                             | `LIKE '%bsd%'`   |       |
| `bsd-dpt`                                | `LIKE '%bsd%'`   |       |
| `bsd-endorsement-allowed`                | `LIKE '%bsd%'`   |       |
| `bsd-export`                             | `LIKE '%bsd%'`   |       |
| `bsd-gnu-efi`                            | `LIKE '%bsd%'`   |       |
| `bsd-inferno-nettverk`                   | `LIKE '%bsd%'`   |       |
| `bsd-innosys`                            | `LIKE '%bsd%'`   |       |
| `bsd-intel`                              | `LIKE '%bsd%'`   |       |
| `bsd-mylex`                              | `LIKE '%bsd%'`   |       |
| `bsd-new`                                | `LIKE '%bsd%'`   |       |
| `bsd-new-derivative`                     | `LIKE '%bsd%'`   |       |
| `bsd-new-far-manager`                    | `LIKE '%bsd%'`   |       |
| `bsd-new-nomod`                          | `LIKE '%bsd%'`   |       |
| `bsd-new-tcpdump`                        | `LIKE '%bsd%'`   |       |
| `bsd-no-disclaimer`                      | `LIKE '%bsd%'`   |       |
| `bsd-no-disclaimer-unmodified`           | `LIKE '%bsd%'`   |       |
| `bsd-original`                           | `LIKE '%bsd%'`   |       |
| `bsd-original-muscle`                    | `LIKE '%bsd%'`   |       |
| `bsd-original-uc-1986`                   | `LIKE '%bsd%'`   |       |
| `bsd-original-uc-1990`                   | `LIKE '%bsd%'`   |       |
| `bsd-original-uc`                        | `LIKE '%bsd%'`   |       |
| `bsd-original-voices`                    | `LIKE '%bsd%'`   |       |
| `bsd-plus-mod-notice`                    | `LIKE '%bsd%'`   |       |
| `bsd-plus-patent`                        | `LIKE '%bsd%'`   |       |
| `bsd-simplified`                         | `LIKE '%bsd%'`   |       |
| `bsd-simplified-darwin`                  | `LIKE '%bsd%'`   |       |
| `bsd-simplified-intel`                   | `LIKE '%bsd%'`   |       |
| `bsd-simplified-source`                  | `LIKE '%bsd%'`   |       |
| `bsd-source-code`                        | `LIKE '%bsd%'`   |       |
| `bsd-systemics`                          | `LIKE '%bsd%'`   |       |
| `bsd-systemics-w3works`                  | `LIKE '%bsd%'`   |       |
| `bsd-top`                                | `LIKE '%bsd%'`   |       |
| `bsd-top-gpl-addition`                   | `LIKE '%bsd%'`   |       |
| `bsd-unchanged`                          | `LIKE '%bsd%'`   |       |
| `bsd-unmodified`                         | `LIKE '%bsd%'`   |       |
| `bsd-x11`                                | `LIKE '%bsd%'`   |       |
| `bsd-zero`                               | `LIKE '%bsd%'`   |       |
| `cc-by-1.0`                              | `LIKE '%cc%'`    |       |
| `cc-by-2.0`                              | exact            |   163 |
| `cc-by-2.0-uk`                           | `LIKE '%cc%'`    |       |
| `cc-by-2.5`                              | exact            |    21 |
| `cc-by-2.5-au`                           | `LIKE '%cc%'`    |       |
| `cc-by-3.0`                              | exact            |   179 |
| `cc-by-3.0-at`                           | `LIKE '%cc%'`    |       |
| `cc-by-3.0-au`                           | `LIKE '%cc%'`    |       |
| `cc-by-3.0-de`                           | `LIKE '%cc%'`    |       |
| `cc-by-3.0-igo`                          | `LIKE '%cc%'`    |       |
| `cc-by-3.0-nl`                           | `LIKE '%cc%'`    |       |
| `cc-by-3.0-us`                           | `LIKE '%cc%'`    |       |
| `cc-by-4.0`                              | `LIKE '%cc%'`    |       |
| `cc-pd`                                  | `LIKE '%cc%'`    |       |
| `cc-pdm-1.0`                             | `LIKE '%cc%'`    |       |
| `cc0-1.0`                                | `LIKE '%cc%'`    |       |
| `cdla-permissive-1.0`                    | exact            |    10 |
| `cdla-permissive-2.0`                    | exact            |    80 |
| `clear-bsd`                              | `LIKE '%bsd%'`   |       |
| `clear-bsd-1-clause`                     | `LIKE '%bsd%'`   |       |
| `dual-bsd-gpl`                           | `LIKE '%bsd%'`   |       |
| `energyplus-bsd`                         | `LIKE '%bsd%'`   |       |
| `etalab-2.0`                             | exact            |    21 |
| `fair`                                   | `LIKE '%fair%'`  |       |
| `freebsd-boot`                           | `LIKE '%bsd%'`   |       |
| `freebsd-doc`                            | `LIKE '%bsd%'`   |       |
| `freebsd-first`                          | `LIKE '%bsd%'`   |       |
| `gareth-mccaughan`                       | `LIKE '%cc%'`    |       |
| `intel-acpi`                             | `LIKE '%intel%'` |       |
| `intel-acpi`                             | `LIKE '%intel%'` |       |
| `intel-bsd`                              | `LIKE '%bsd%'`   |       |
| `intel-bsd-2-clause`                     | `LIKE '%bsd%'`   |       |
| `intel-bsd-export-control`               | `LIKE '%bsd%'`   |       |
| `intel-osl-1989`                         | `LIKE '%intel%'` |       |
| `intel-osl-1993`                         | `LIKE '%intel%'` |       |
| `lbnl-bsd`                               | `LIKE '%bsd%'`   |       |
| `lanl-bsd-3-variant`                     | `LIKE '%bsd%'`   |       |
| `morbig-ieee-std-usage`                  | `LIKE '%big%'`   |       |
| `odc-by-1.0`                             | `LIKE '%odc%'`   |       |
| `pddl-1.0`.                              | `LIKE '%pddl%'`  |       |
| `purdue-bsd`                             | `LIKE '%bsd%'`   |       |
| `red-hat-bsd-simplified`                 | `LIKE '%bsd%'`   |       |
| `ricebsd`                                | `LIKE '%bsd%'`   |       |
| `w3c-03-bsd-license`                     | `LIKE '%bsd%'`   |       |

## So, Which Licenses Can We "Recover"??

Comparing this list to `bad-licenses.json`, the following bad licenses appear to map to known permissive licenses.

| "Bad" License Key     | Match        | Count |
| :-------------------- | :----------- | ----: |
| `cc-by-2.0`           | same         |   163 |
| `cc-by-2.5`           | same         |    21 |
| `cc-by-3.0`           | same         |   179 |
| `cdla-permissive-1.0` | same         |    10 |
| `cdla-permissive-2.0` | same         |    80 |
| `etalab-2.0`          | same         |    21 |
| `odc-by`              | `odc-by-1.0` |   179 |
| `pddl`                | `pddl-1.0`   |    67 |
|                       | **Total:**   | **720** |

Recall that these license keys were extracted from `choosealicense.com` URLs.

These keys are less clear:

| "Bad" License Key     | Match?                 | Count |
| :-------------------- | :--------------------- | ----: |
| `cc`                  | `cc-by-2.0`?           |   618 |
| `bsd`                 | unclear which one?     |   137 |
| `cdla-sharing-1.0`    | `cdla-permissive-2.0`? |    57 |
|                       | **Total:**             | **812** |


## All Acceptable Licenses 

Using `LIKE` clauses allowed us to _fuzzy match_ some license keys that appear in some datasets with a _likely_ "official" license key, but it is imperfect. For example, just saying `bsd` could be interpreted to mean one of the many permissive variants, but this assumption could be wrong.

Let's just find all the `scancode_licenses` that are `Permissive` or `Public Domain`:

```sql
CREATE OR REPLACE TABLE all_permissive_licenses AS
SELECT *
FROM scancode_licenses
WHERE  category = 'Permissive' OR category = 'Public Domain';

COPY all_permissive_licenses TO 'all-permissive-licenses.json';
```

This table has 1009 rows.

## Can We Create "The Ultimate query"??

```sql
CREATE OR REPLACE TABLE all_hf_licenses AS
SELECT DISTINCT  
  hfm_id,
  hfm_real_license_id,
  hfm_license_id,
  hfm_license,
  hfm_license_url,
  license_key,
  category,
  license
FROM (
  SELECT
    rtrim(regexp_replace(license_url, 'https://choosealicense.com/licenses/', ''), '/') AS hfm_id,
    CASE 
      WHEN hfm_id = 'odc-by'  THEN 'odc-by-1.0'
      WHEN hfm_id = 'pddl'    THEN 'pddl-1.0'
      ELSE hfm_id
    END AS hfm_real_license_id,
    license_id  AS hfm_license_id,
    license     AS hfm_license,
    license_url AS hfm_license_url 
  FROM hf_metadata_with_bad_licenses)
JOIN (
  SELECT
    license_key,
    category,
    license
  FROM scancode_licenses)
ON lower(license_key) = hfm_real_license_id
ORDER BY hfm_real_license_id ASC;

COPY all_hf_licenses TO 'all-hf-licenses.json';
```

This has 45 rows. What about just the permissive licenses?

```sql
CREATE OR REPLACE TABLE all_hf_permissive_licenses AS
SELECT * FROM all_hf_licenses
WHERE  category = 'Permissive' OR category = 'Public Domain'
ORDER BY hfm_real_license_id ASC;

SELECT count() FROM all_hf_permissive_licenses;

COPY all_hf_permissive_licenses TO 'all-hf-permissive-licenses.json';
```

This returns 19 rows.

## Recap: How to Find the Permissive Datasets

First, in `hf_metadata_with_bad_licenses`, if `license_id` isn't `NULL`, then the id extracted from the URL is _identical_ to `license_id`. The following query returns zero rows:

```sql
SELECT
  hfm_id, license_id, count
FROM (
  SELECT 
    rtrim(regexp_replace(license_url, 'https://choosealicense.com/licenses/', ''), '/') AS hfm_id,
    license_id,
    count() AS count
  FROM hf_metadata_with_bad_licenses
  GROUP BY license_id, hfm_id
  ORDER BY count DESC)
WHERE license_id NOT NULL AND license_id <> hfm_id;
```

This effectively means we can ignore `license_id` as it is redundant with the constructed `hfm_id`, which has more values not `NULL`.

```sql
SELECT 
  rtrim(regexp_replace(license_url, 'https://choosealicense.com/licenses/', ''), '/') AS hfm_id,
  count() AS count
FROM hf_metadata_with_bad_licenses
GROUP BY hfm_id
ORDER BY count DESC;
```

This has 78 rows. To determine which are permissive:

```sql
CREATE OR REPLACE TABLE hf_good_licenses_counts AS
SELECT 
  hfm.id, hfm_real_license_id, count() AS count
FROM (
  SELECT 
    rtrim(regexp_replace(license_url, 'https://choosealicense.com/licenses/', ''), '/') AS id,
  FROM hf_metadata_with_bad_licenses
  WHERE id NOT NULL) AS hfm
JOIN all_hf_permissive_licenses AS perm
ON   hfm.id = perm.hfm_id
GROUP BY hfm.id, hfm_real_license_id
ORDER BY count DESC;

COPY hf_good_licenses_counts TO 'hf-good-licenses-counts.json';

SELECT * FROM hf_good_licenses_counts;
┌─────────────────────┬─────────────────────┬───────┐
│         id          │ hfm_real_license_id │ count │
│       varchar       │       varchar       │ int64 │
├─────────────────────┼─────────────────────┼───────┤
│ apache-2.0          │ apache-2.0          │ 28229 │
│ mit                 │ mit                 │ 21019 │
│ cc-by-4.0           │ cc-by-4.0           │  5052 │
│ cc0-1.0             │ cc0-1.0             │  1157 │
│ odc-by              │ odc-by-1.0          │   618 │
│ afl-3.0             │ afl-3.0             │   424 │
│ cc-by-3.0           │ cc-by-3.0           │   179 │
│ cc-by-2.0           │ cc-by-2.0           │   163 │
│ unlicense           │ unlicense           │   150 │
│ cdla-permissive-2.0 │ cdla-permissive-2.0 │    80 │
│ pddl                │ pddl-1.0            │    67 │
│ cc-by-2.5           │ cc-by-2.5           │    21 │
│ etalab-2.0          │ etalab-2.0          │    21 │
│ ecl-2.0             │ ecl-2.0             │    12 │
│ ms-pl               │ ms-pl               │    12 │
│ cdla-permissive-1.0 │ cdla-permissive-1.0 │    10 │
│ postgresql          │ postgresql          │     9 │
│ zlib                │ zlib                │     2 │
│ isc                 │ isc                 │     2 │
├─────────────────────┴─────────────────────┴───────┤
│ 19 rows                                 3 columns │
└───────────────────────────────────────────────────┘
```

> **NOTE:** `unlicense` is a [real, premissive license](https://choosealicense.com/licenses/unlicense/), not the same as _no license_.

Compare this result to just looking at `hf_metadata` with valid `license_id`s:

```sql
SELECT 
  license_id, count() AS count
FROM (
  SELECT license_id 
  FROM hf_metadata
  WHERE license_id NOT NULL)
JOIN all_hf_permissive_licenses AS perm
ON   license_id = perm.hfm_id
GROUP BY license_id
ORDER BY count DESC;
┌────────────┬───────┐
│ license_id │ count │
│  varchar   │ int64 │
├────────────┼───────┤
│ apache-2.0 │ 28229 │
│ mit        │ 21019 │
│ cc-by-4.0  │  5052 │
│ cc0-1.0    │  1157 │
│ afl-3.0    │   424 │
│ unlicense  │   150 │
│ ecl-2.0    │    12 │
│ ms-pl      │    12 │
│ postgresql │     9 │
│ zlib       │     2 │
│ isc        │     2 │
├────────────┴───────┤
│ 11 rows  2 columns │
└────────────────────┘
```

We can pick up **eight** more licenses and **1159** more datasets.

| `id`                  | `hfm_real_license_id`   |  count |
| :-------------------- | :---------------------- | -----: |
| `odc-by`              | `odc-by-1.0`            |    618 |
| `cc-by-3.0`           | `cc-by-3.0`             |    179 |
| `cc-by-2.0`           | `cc-by-2.0`             |    163 |
| `cdla-permissive-2.0` | `cdla-permissive-2.0`   |     80 |
| `pddl`                | `pddl-1.0`              |     67 |
| `cc-by-2.5`           | `cc-by-2.5`             |     21 |
| `etalab-2.0`          | `etalab-2.0`            |     21 |
| `cdla-permissive-1.0` | `cdla-permissive-1.0`   |     10 |
|                       | **Total:**              |**1159**|
