// Load libraries
import angular from 'angular';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';

import LoginController from 'src/LoginController';
import MonitorController from 'src/MonitorController';
import SettingsController from 'src/SettingsController';
import GlobalController from 'src/GlobalController';

export default angular.module( 'starter-app', [ 'ngMaterial' ] )
  .config(($mdIconProvider, $mdThemingProvider) => {
    // Register the user `avatar` icons
    $mdIconProvider
      .defaultIconSet("./assets/svg/avatars.svg", 128)
      .icon("menu", "./assets/svg/menu.svg", 24)

    $mdThemingProvider.theme('default')
      .primaryPalette('blue-grey')
      .accentPalette('orange');
  })
  .controller('LoginController', LoginController)
  .controller('MonitorController', MonitorController)
  .controller('SettingsController', SettingsController)
  .controller('GlobalController', GlobalController);
