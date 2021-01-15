
import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';
export default [
{
  path: '/',
  component: ComponentCreator('/','deb'),
  exact: true,
},
{
  path: '/__docusaurus/debug',
  component: ComponentCreator('/__docusaurus/debug','3d6'),
  exact: true,
},
{
  path: '/__docusaurus/debug/config',
  component: ComponentCreator('/__docusaurus/debug/config','914'),
  exact: true,
},
{
  path: '/__docusaurus/debug/content',
  component: ComponentCreator('/__docusaurus/debug/content','c28'),
  exact: true,
},
{
  path: '/__docusaurus/debug/globalData',
  component: ComponentCreator('/__docusaurus/debug/globalData','3cf'),
  exact: true,
},
{
  path: '/__docusaurus/debug/metadata',
  component: ComponentCreator('/__docusaurus/debug/metadata','31b'),
  exact: true,
},
{
  path: '/__docusaurus/debug/registry',
  component: ComponentCreator('/__docusaurus/debug/registry','0da'),
  exact: true,
},
{
  path: '/__docusaurus/debug/routes',
  component: ComponentCreator('/__docusaurus/debug/routes','244'),
  exact: true,
},
{
  path: '/docs',
  component: ComponentCreator('/docs','460'),
  
  routes: [
{
  path: '/docs/',
  component: ComponentCreator('/docs/','87d'),
  exact: true,
},
{
  path: '/docs/',
  component: ComponentCreator('/docs/','2b5'),
  exact: true,
},
{
  path: '/docs/doc3',
  component: ComponentCreator('/docs/doc3','e02'),
  exact: true,
},
{
  path: '/docs/docs/doc3',
  component: ComponentCreator('/docs/docs/doc3','f6e'),
  exact: true,
},
{
  path: '/docs/docs/gettingstarted',
  component: ComponentCreator('/docs/docs/gettingstarted','9e3'),
  exact: true,
},
{
  path: '/docs/docs/intro',
  component: ComponentCreator('/docs/docs/intro','6a2'),
  exact: true,
},
{
  path: '/docs/docs/mdx',
  component: ComponentCreator('/docs/docs/mdx','78f'),
  exact: true,
},
{
  path: '/docs/gettingstarted',
  component: ComponentCreator('/docs/gettingstarted','940'),
  exact: true,
},
{
  path: '/docs/intro',
  component: ComponentCreator('/docs/intro','3d9'),
  exact: true,
},
{
  path: '/docs/mdx',
  component: ComponentCreator('/docs/mdx','955'),
  exact: true,
},
{
  path: '/docs/README',
  component: ComponentCreator('/docs/README','c42'),
  exact: true,
},
]
},
{
  path: '*',
  component: ComponentCreator('*')
}
];
