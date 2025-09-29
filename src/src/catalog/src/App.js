import React, { useState } from 'react';
import './App.css';
import { Heading, Button, Flex, View, TextField, Text, Image, SliderField, SelectField } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import athenaService from './services/athenaService';
import QueryResultsTable from './components/QueryResultsTable';

function App() {
  const [queryResults, setQueryResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchText, setSearchText] = useState('');
  const [orgText, setOrgText] = useState('');
  const [language, setLanguage] = useState('');
  const [license, setLicense] = useState('');
  const [minScore, setMinScore] = useState(0);

  var license_clause = "";
  if (license) {
    license_clause = `d.license like '${license}' and `
  }
  
  var language_clause = "";
  if (language) {
    language_clause = `contains(d.tags, 'language:${language}') and `
  }

  var tag_clause = "";
  if (searchText) {
    tag_clause = `contains(d.tags, '${searchText}') and `
  }

  var org_clause = "";
  if (orgText) {
    org_clause = `lower(d.author) like '${orgText}%' and `
  }


  const resetForm = () => {
    setSearchText('');
    setLanguage('');
    setLicense('');
    setLicense('');
    setOrgText('');
    setMinScore(0);
    setQueryResults(null);
    setError(null);
  };

  const executeQuery = async () => {
    setLoading(true);
    setError(null);
    setQueryResults(null);

    const dynamicQuery2 = `
    select 
        concat('[',o.dataset,'](https://huggingface.co/datasets/',o.dataset,')') as "Data Set",
        array_join(d.tags, ', ') as "Tags",
        o.license as "License",
        o.score as "OTDI Score",
        o.notes as "Scoring Justification"
    from aialliance.otdi o
    left join huggingface.v_datasets d  on o.dataset = d.dataset
    where 
      ${license_clause}
      ${language_clause}
      ${tag_clause}
      ${org_clause}
      score >= ${minScore} 
    order by o.score desc
    limit 100    
    `;



    try {
      const results = await athenaService.executeQuery(dynamicQuery2);
      setQueryResults(results);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <Flex direction="row" gap="1rem" alignItems="center">
          <Heading level={1}>NextGem Data Catalog</Heading>
          <Image
            src="/nextgem_logo.png"
            alt="NextGem Logo"
            height="135px"
          />
        </Flex>
        <View marginTop="2rem">
          <Flex direction="row" gap="2rem" alignItems="flex-start" justifyContent="center">
            <View>
              <Text fontWeight="bold" marginBottom="0.5rem" fontSize="0.8em">OTDI Minimum Score</Text>
              <SliderField
                label=""
                min={0}
                max={100}
                step={1}
                value={minScore}
                onChange={setMinScore}
                width="200px"
              />
              <TextField
                value={minScore}
                onChange={(e) => setMinScore(Number(e.target.value))}
                type="number"
                min={0}
                max={100}
                width="80px"
                marginTop="0.5rem"
              />
              <Text fontSize="0.6em" marginTop="0.5rem">
                <a href="https://the-ai-alliance.github.io/open-trusted-data-initiative/dataset-requirements/" target="_blank" rel="noopener noreferrer">
                  About the OTDI Spec
                </a>
              </Text>
            </View>
            <View>
              <Flex direction="column" gap="1rem" alignItems="center">
                <TextField
                  value={searchText}
                  onChange={(e) => setSearchText(e.target.value)}
                  placeholder="Enter a use case (e.g. legal, finance, chemisty...)"
                  width="400px"
                />
                <TextField
                  value={orgText}
                  onChange={(e) => setOrgText(e.target.value)}
                  placeholder="Enter an organization"
                  width="400px"
                />
                <SelectField
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  placeholder="Select a language..."
                  width="400px"
                >
                  <option value="ab">Abkhazian</option>
                  <option value="aa">Afar</option>
                  <option value="af">Afrikaans</option>
                  <option value="ak">Akan</option>
                  <option value="sq">Albanian</option>
                  <option value="am">Amharic</option>
                  <option value="ar">Arabic</option>
                  <option value="an">Aragonese</option>
                  <option value="hy">Armenian</option>
                  <option value="as">Assamese</option>
                  <option value="av">Avaric</option>
                  <option value="ae">Avestan</option>
                  <option value="ay">Aymara</option>
                  <option value="az">Azerbaijani</option>
                  <option value="bm">Bambara</option>
                  <option value="ba">Bashkir</option>
                  <option value="eu">Basque</option>
                  <option value="be">Belarusian</option>
                  <option value="bn">Bengali</option>
                  <option value="bi">Bislama</option>
                  <option value="bs">Bosnian</option>
                  <option value="br">Breton</option>
                  <option value="bg">Bulgarian</option>
                  <option value="my">Burmese</option>
                  <option value="ca">Catalan, Valencian</option>
                  <option value="km">Central Khmer</option>
                  <option value="ch">Chamorro</option>
                  <option value="ce">Chechen</option>
                  <option value="ny">Chichewa, Chewa, Nyanja</option>
                  <option value="zh">Chinese</option>
                  <option value="cu">Church Slavonic</option>
                  <option value="cv">Chuvash</option>
                  <option value="kw">Cornish</option>
                  <option value="co">Corsican</option>
                  <option value="cr">Cree</option>
                  <option value="hr">Croatian</option>
                  <option value="cs">Czech</option>
                  <option value="da">Danish</option>
                  <option value="dv">Divehi, Dhivehi, Maldivian</option>
                  <option value="nl">Dutch, Flemish</option>
                  <option value="dz">Dzongkha</option>
                  <option value="en">English</option>
                  <option value="eo">Esperanto</option>
                  <option value="et">Estonian</option>
                  <option value="ee">Ewe</option>
                  <option value="fo">Faroese</option>
                  <option value="fj">Fijian</option>
                  <option value="fi">Finnish</option>
                  <option value="fr">French</option>
                  <option value="ff">Fulah</option>
                  <option value="gd">Gaelic, Scottish Gaelic</option>
                  <option value="gl">Galician</option>
                  <option value="lg">Ganda</option>
                  <option value="ka">Georgian</option>
                  <option value="de">German</option>
                  <option value="el">Greek, Modern (1453–)</option>
                  <option value="gn">Guarani</option>
                  <option value="gu">Gujarati</option>
                  <option value="ht">Haitian, Haitian Creole</option>
                  <option value="ha">Hausa</option>
                  <option value="he">Hebrew</option>
                  <option value="hz">Herero</option>
                  <option value="hi">Hindi</option>
                  <option value="ho">Hiri Motu</option>
                  <option value="hu">Hungarian</option>
                  <option value="is">Icelandic</option>
                  <option value="io">Ido</option>
                  <option value="ig">Igbo</option>
                  <option value="id">Indonesian</option>
                  <option value="ia">Interlingua</option>
                  <option value="ie">Interlingue, Occidental</option>
                  <option value="iu">Inuktitut</option>
                  <option value="ik">Inupiaq</option>
                  <option value="ga">Irish</option>
                  <option value="it">Italian</option>
                  <option value="ja">Japanese</option>
                  <option value="jv">Javanese</option>
                  <option value="kl">Kalaallisut, Greenlandic</option>
                  <option value="kn">Kannada</option>
                  <option value="kr">Kanuri</option>
                  <option value="ks">Kashmiri</option>
                  <option value="kk">Kazakh</option>
                  <option value="ki">Kikuyu, Gikuyu</option>
                  <option value="rw">Kinyarwanda</option>
                  <option value="kv">Komi</option>
                  <option value="kg">Kongo</option>
                  <option value="ko">Korean</option>
                  <option value="kj">Kuanyama, Kwanyama</option>
                  <option value="ku">Kurdish</option>
                  <option value="ky">Kyrgyz, Kirghiz</option>
                  <option value="lo">Lao</option>
                  <option value="la">Latin</option>
                  <option value="lv">Latvian</option>
                  <option value="li">Limburgan, Limburger, Limburgish</option>
                  <option value="ln">Lingala</option>
                  <option value="lt">Lithuanian</option>
                  <option value="lu">Luba-Katanga</option>
                  <option value="lb">Luxembourgish, Letzeburgesch</option>
                  <option value="mk">Macedonian</option>
                  <option value="mg">Malagasy</option>
                  <option value="ms">Malay</option>
                  <option value="ml">Malayalam</option>
                  <option value="mt">Maltese</option>
                  <option value="gv">Manx</option>
                  <option value="mi">Maori</option>
                  <option value="mr">Marathi</option>
                  <option value="mh">Marshallese</option>
                  <option value="mn">Mongolian</option>
                  <option value="na">Nauru</option>
                  <option value="nv">Navajo, Navaho</option>
                  <option value="ng">Ndonga</option>
                  <option value="ne">Nepali</option>
                  <option value="nd">North Ndebele</option>
                  <option value="se">Northern Sami</option>
                  <option value="no">Norwegian</option>
                  <option value="nb">Norwegian Bokmål</option>
                  <option value="nn">Norwegian Nynorsk</option>
                  <option value="oc">Occitan</option>
                  <option value="oj">Ojibwa</option>
                  <option value="or">Oriya</option>
                  <option value="om">Oromo</option>
                  <option value="os">Ossetian, Ossetic</option>
                  <option value="pi">Pali</option>
                  <option value="ps">Pashto, Pushto</option>
                  <option value="fa">Persian</option>
                  <option value="pl">Polish</option>
                  <option value="pt">Portuguese</option>
                  <option value="pa">Punjabi, Panjabi</option>
                  <option value="qu">Quechua</option>
                  <option value="ro">Romanian, Moldavian, Moldovan</option>
                  <option value="rm">Romansh</option>
                  <option value="rn">Rundi</option>
                  <option value="ru">Russian</option>
                  <option value="sm">Samoan</option>
                  <option value="sg">Sango</option>
                  <option value="sa">Sanskrit</option>
                  <option value="sc">Sardinian</option>
                  <option value="sr">Serbian</option>
                  <option value="sn">Shona</option>
                  <option value="ii">Sichuan Yi, Nuosu</option>
                  <option value="sd">Sindhi</option>
                  <option value="si">Sinhala, Sinhalese</option>
                  <option value="sk">Slovak</option>
                  <option value="sl">Slovenian</option>
                  <option value="so">Somali</option>
                  <option value="nr">South Ndebele</option>
                  <option value="st">Southern Sotho</option>
                  <option value="es">Spanish, Castilian</option>
                  <option value="su">Sundanese</option>
                  <option value="sw">Swahili</option>
                  <option value="ss">Swati</option>
                  <option value="sv">Swedish</option>
                  <option value="tl">Tagalog</option>
                  <option value="ty">Tahitian</option>
                  <option value="tg">Tajik</option>
                  <option value="ta">Tamil</option>
                  <option value="tt">Tatar</option>
                  <option value="te">Telugu</option>
                  <option value="th">Thai</option>
                  <option value="bo">Tibetan</option>
                  <option value="ti">Tigrinya</option>
                  <option value="to">Tonga (Tonga Islands)</option>
                  <option value="ts">Tsonga</option>
                  <option value="tn">Tswana</option>
                  <option value="tr">Turkish</option>
                  <option value="tk">Turkmen</option>
                  <option value="tw">Twi</option>
                  <option value="ug">Uighur, Uyghur</option>
                  <option value="uk">Ukrainian</option>
                  <option value="ur">Urdu</option>
                  <option value="uz">Uzbek</option>
                  <option value="ve">Venda</option>
                  <option value="vi">Vietnamese</option>
                  <option value="vo">Volapük</option>
                  <option value="wa">Walloon</option>
                  <option value="cy">Welsh</option>
                  <option value="fy">Western Frisian</option>
                  <option value="wo">Wolof</option>
                  <option value="xh">Xhosa</option>
                  <option value="yi">Yiddish</option>
                  <option value="yo">Yoruba</option>
                  <option value="za">Zhuang, Chuang</option>
                  <option value="zu">Zulu</option>
                </SelectField>
                <SelectField
                  value={license}
                  onChange={(e) => setLicense(e.target.value)}
                  placeholder="Select a license..."
                  width="400px"
                >
                  <option value="afl%">Academic Free</option>
                  <option value="apache%">Apache 2.0</option>
                  <option value="bsd%">BSD</option>
                  <option value="cc%">Creative Commons | Any version</option>
                  <option value="cc%4.0">Creative Commons | ver 4.0</option>
                  <option value="cc%3.0">Creative Commons | ver 3.0</option>
                  <option value="cc%2.0">Creative Commons | ver 2.0</option>
                  <option value="cc0-1.0">Creative Commons | ver 1.0</option>
                  <option value="gpl%">GPL | Any version</option>
                  <option value="gpl-3.0%">GPL | ver 3.0</option>
                  <option value="gpl-2.0%">GPL | ver 2.0</option>
                  <option value="llama%">Llama</option>
                  <option value="odc%">Open Data Commons</option>
                  <option value="%openrail%">OpenRAIL</option>
                  <option value="mit%">MIT</option>
                </SelectField>
                <Flex direction="row" gap="1rem">
                  <Button onClick={executeQuery} disabled={loading}>
                    {loading ? 'Executing Query...' : 'Search Catalog'}
                  </Button>
                  <Button variation="secondary" onClick={resetForm}>
                    Reset
                  </Button>
                </Flex>
              </Flex>
            </View>
          </Flex>
            <View marginTop="2rem" width="100%">
              <QueryResultsTable 
                data={queryResults} 
                loading={loading} 
                error={error}
              /> 
            </View>
        </View>
      </header>
    </div>
  );
}

export default App;
