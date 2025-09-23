import React, { useState } from 'react';
import './App.css';
import { Heading, Button, Flex, View, TextField, Text, Image, SliderField } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import athenaService from './services/athenaService';
import QueryResultsTable from './components/QueryResultsTable';

function App() {
  const [queryResults, setQueryResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchText, setSearchText] = useState('');
  const [language, setLanguage] = useState('');
  const [license, setLicense] = useState('');
  const [minScore, setMinScore] = useState(0);

  var clause1 = "";
  if (license) {
    clause1 = `contains(d.tags, 'license:${license}') and `
  }
  
  var clause2 = "";
  if (language) {
    clause2 = `contains(d.tags, 'language:${language}') and `
  }

  var clause3 = "";
  if (searchText) {
    clause3 = `contains(d.tags, '${searchText}') and `
  }


  const resetForm = () => {
    setSearchText('');
    setLanguage('');
    setLicense('');
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
    left join huggingface.datasets d  on o.dataset = d.dataset
    where 
      o.date = cast('2025-06-29' as date) and 
      d.date = cast('2025-09-09' as date) and
      ${clause1}
      ${clause2}
      ${clause3}
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
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  placeholder="Enter a language (e.g. en, fr, it...)"
                  width="400px"
                />
                <Text fontSize="0.6em">
                  <a href="https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes" target="_blank" rel="noopener noreferrer">
                    List of valid languages. Use column 'Set 1'.
                  </a>
                </Text>
                <TextField
                  value={license}
                  onChange={(e) => setLicense(e.target.value)}
                  placeholder="Enter a license..."
                  width="400px"
                />
                <Text fontSize="0.6em">
                  <a href="https://huggingface.co/docs/hub/repositories-licenses" target="_blank" rel="noopener noreferrer">
                    List of valid licenses. Use column 'license identifier'.
                  </a>
                </Text>
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
