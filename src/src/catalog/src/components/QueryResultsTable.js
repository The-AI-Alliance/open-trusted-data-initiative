import React, { useState, useEffect } from 'react';
import { Table, TableHead, TableBody, TableRow, TableCell, Link, Button, Flex, Text } from '@aws-amplify/ui-react';

const QueryResultsTable = ({ data, loading, error }) => {
  const [currentPage, setCurrentPage] = useState(0);
  const pageSize = 20;

  useEffect(() => {
    setCurrentPage(0);
  }, [data]);

  if (loading) {
    return <div>Loading query results...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error.message}</div>;
  }

  if (!data || !data.columns || data.columns.length === 0) {
    return <div>No data to display</div>;
  }

  const totalPages = Math.ceil(data.rows.length / pageSize);
  const startIndex = currentPage * pageSize;
  const endIndex = startIndex + pageSize;
  const currentPageData = data.rows.slice(startIndex, endIndex);

  const parseMarkdownLink = (text) => {
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/;
    const match = text.match(linkRegex);

    if (match) {
      const [, linkText, url] = match;
      return { text: linkText, url: url };
    }

    return { text: text, url: null };
  };

  const handlePreviousPage = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <div>
      <Table variation="striped">
        <TableHead>
          <TableRow>
            {data.columns.map((column, index) => (
              <TableCell key={index} as="th">
                {column}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {currentPageData.map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              {row.map((cell, cellIndex) => {
                if (cellIndex === 0) {
                  const { text, url } = parseMarkdownLink(cell);
                  return (
                    <TableCell key={cellIndex} textAlign="left">
                      {url ? (
                        <Link href={url} target="_blank" rel="noopener noreferrer">
                          {text}
                        </Link>
                      ) : (
                        cell
                      )}
                    </TableCell>
                  );
                }
                return (
                  <TableCell key={cellIndex}>
                    {cell}
                  </TableCell>
                );
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {totalPages > 1 && (
        <Flex 
          justifyContent="space-between" 
          alignItems="center" 
          marginTop="medium"
          paddingX="small"
        >
          <Button 
            variation="primary" 
            onClick={handlePreviousPage} 
            isDisabled={currentPage === 0}
          >
            Previous
          </Button>
          
          <Text>
            Page {currentPage + 1} of {totalPages} ({data.rows.length} total records)
          </Text>
          
          <Button 
            variation="primary" 
            onClick={handleNextPage} 
            isDisabled={currentPage === totalPages - 1}
          >
            Next
          </Button>
        </Flex>
      )}
    </div>
  );
};

export default QueryResultsTable;