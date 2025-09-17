import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const I18nDebugPanel = () => {
  const { t, i18n } = useTranslation();
  const [apiStatus, setApiStatus] = useState('checking...');
  const [apiData, setApiData] = useState(null);

  const testAPI = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/language-info/', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setApiData(data);
        setApiStatus('✅ Connected');
      } else {
        setApiStatus(`❌ Error: ${response.status}`);
      }
    } catch (error) {
      setApiStatus(`❌ Failed: ${error.message}`);
    }
  };

  const testTranslationsAPI = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/translations/', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Translations from API:', data);
      }
    } catch (error) {
      console.error('Translations API error:', error);
    }
  };

  const changeLanguage = async (lang: string) => {
    try {
      // Change in i18next
      await i18n.changeLanguage(lang);
      
      // Notify backend
      await fetch('http://localhost:8000/api/v1/set-language/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ language: lang }),
      });
      
      console.log(`Language changed to: ${lang}`);
    } catch (error) {
      console.error('Error changing language:', error);
    }
  };

  useEffect(() => {
    testAPI();
    testTranslationsAPI();
  }, []);

  return (
    <Card className="m-4 max-w-md">
      <CardHeader>
        <CardTitle>🌐 i18n Debug Panel</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <strong>API Status:</strong> {apiStatus}
        </div>
        
        <div>
          <strong>Current Language:</strong> {i18n.language}
        </div>
        
        <div>
          <strong>Sample Translations:</strong>
          <ul className="text-sm">
            <li>nav.home: {t('nav.home')}</li>
            <li>hero.title: {t('hero.title')}</li>
            <li>products.ggp: {t('products.ggp')}</li>
          </ul>
        </div>
        
        <div className="space-x-2">
          <Button 
            size="sm" 
            onClick={() => changeLanguage('vi')}
            variant={i18n.language === 'vi' ? 'default' : 'outline'}
          >
            VI
          </Button>
          <Button 
            size="sm" 
            onClick={() => changeLanguage('en')}
            variant={i18n.language === 'en' ? 'default' : 'outline'}
          >
            EN
          </Button>
        </div>
        
        <Button size="sm" onClick={testAPI} variant="outline" className="w-full">
          Test API Connection
        </Button>
        
        {apiData && (
          <div className="text-xs bg-gray-100 p-2 rounded">
            <pre>{JSON.stringify(apiData, null, 2)}</pre>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default I18nDebugPanel;
