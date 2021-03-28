
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
  component: ComponentCreator('/docs','803'),
  
  routes: [
{
  path: '/docs/',
  component: ComponentCreator('/docs/','40c'),
  exact: true,
},
{
  path: '/docs/datadict',
  component: ComponentCreator('/docs/datadict','e46'),
  exact: true,
},
{
  path: '/docs/functions',
  component: ComponentCreator('/docs/functions','478'),
  exact: true,
},
{
  path: '/docs/hardware',
  component: ComponentCreator('/docs/hardware','bee'),
  exact: true,
},
{
  path: '/docs/modules',
  component: ComponentCreator('/docs/modules','191'),
  exact: true,
},
{
  path: '/docs/sourcecode',
  component: ComponentCreator('/docs/sourcecode','4e0'),
  exact: true,
},
{
  path: '/docs/synopsis',
  component: ComponentCreator('/docs/synopsis','e8f'),
  exact: true,
},
]
},
{
  path: '*',
  component: ComponentCreator('*')
}
];
