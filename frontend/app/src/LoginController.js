/**
 * Main App Controller for the Angular Material Starter App
 * @param UsersDataService
 * @param $mdSidenav
 * @constructor
 */
function LoginController($mdSidenav, $window) {
  var self = this;
  self.login = function(){
    $window.location.href = '/login';
  };
}

export default [ '$mdSidenav', '$window', LoginController ];
