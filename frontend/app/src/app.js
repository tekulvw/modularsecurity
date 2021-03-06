// Load libraries
import angular from 'angular';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';

import LoginController from 'src/LoginController';
import MonitorController from 'src/MonitorController';
import ManageController from 'src/ManageController';
import SettingsController from 'src/SettingsController';
import GlobalController from 'src/GlobalController';

export default angular.module( 'starter-app', [ 'ngMaterial' ] )
  .config(($mdIconProvider, $mdThemingProvider) => {

    $mdIconProvider.fontSet('md', 'material-icons');

    $mdThemingProvider.theme('default')
      .primaryPalette('blue-grey')
      .accentPalette('orange');
  })
  .controller('LoginController', LoginController)
  .controller('MonitorController', MonitorController)
  .controller('ManageController', ManageController)
  .controller('SettingsController', SettingsController)
  .controller('GlobalController', GlobalController);
