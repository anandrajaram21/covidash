/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'Covidash',
  tagline: 'An open source, community driver, COVID-19 dashboard',
  url: 'https://anandrajaram21.github.io/covidash',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'anandrajaram21', // Usually your GitHub org/user name.
  projectName: 'covidash', // Usually your repo name.
  themeConfig: {
    navbar: {
      title: 'Covidash',
      logo: {
        alt: 'Covidash',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: 'docs/',
          activeBasePath: 'docs',
          label: 'Docs',
          position: 'left',
        },
        {
          href: 'https://github.com/anandrajaram21/covidash',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/anandrajaram21/covidash',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/anandrajaram21/covidash',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
