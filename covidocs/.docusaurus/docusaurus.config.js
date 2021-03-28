export default {
  "title": "Covidash",
  "tagline": "An open source, community driver, COVID-19 dashboard",
  "url": "https://anandrajaram21.github.io/covidash",
  "baseUrl": "/",
  "onBrokenLinks": "throw",
  "onBrokenMarkdownLinks": "warn",
  "favicon": "img/favicon.ico",
  "organizationName": "anandrajaram21",
  "projectName": "covidash",
  "themeConfig": {
    "navbar": {
      "title": "Covidash",
      "logo": {
        "alt": "Covidash",
        "src": "img/logo.svg"
      },
      "items": [
        {
          "to": "docs/",
          "activeBasePath": "docs",
          "label": "Docs",
          "position": "left"
        },
        {
          "href": "https://github.com/anandrajaram21/covidash",
          "label": "GitHub",
          "position": "right"
        }
      ],
      "hideOnScroll": false
    },
    "colorMode": {
      "defaultMode": "light",
      "disableSwitch": false,
      "respectPrefersColorScheme": false,
      "switchConfig": {
        "darkIcon": "🌜",
        "darkIconStyle": {},
        "lightIcon": "🌞",
        "lightIconStyle": {}
      }
    },
    "docs": {
      "versionPersistence": "localStorage"
    },
    "metadatas": [],
    "prism": {
      "additionalLanguages": []
    },
    "hideableSidebar": false
  },
  "presets": [
    [
      "@docusaurus/preset-classic",
      {
        "docs": {
          "sidebarPath": "/home/anand/Computer Science/covidash/covidocs/sidebars.js",
          "editUrl": "https://github.com/anandrajaram21/covidash"
        },
        "blog": {
          "showReadingTime": true,
          "editUrl": "https://github.com/anandrajaram21/covidash"
        },
        "theme": {
          "customCss": "/home/anand/Computer Science/covidash/covidocs/src/css/custom.css"
        }
      }
    ]
  ],
  "baseUrlIssueBanner": true,
  "i18n": {
    "defaultLocale": "en",
    "locales": [
      "en"
    ],
    "localeConfigs": {}
  },
  "onDuplicateRoutes": "warn",
  "customFields": {},
  "plugins": [],
  "themes": [],
  "titleDelimiter": "|",
  "noIndex": false
};