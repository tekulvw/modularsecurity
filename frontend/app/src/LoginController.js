function LoginController($mdSidenav, $window) {
  var self = this;
  self.login = function(){
    $window.location.href = '/api/login';
  };
}

export default [ '$mdSidenav', '$window', LoginController ];
