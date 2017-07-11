function ManageController($mdDialog) {
  var self = this;
  self.addDevice = function(ev) {
    // Appending dialog to document.body to cover sidenav in docs app
    var confirm = $mdDialog.prompt()
      .title('Enter Device Serial Number')
      .placeholder('Serial Number')
      .targetEvent(ev)
      .ok('Enter')
      .cancel('Cancel');

    $mdDialog.show(confirm).then(function(result) {
      console.log("Device Set: "+ result);
    }, function() {
    });
  };

  self.addSecondary = function(ev) {
    // Appending dialog to document.body to cover sidenav in docs app
    var confirm = $mdDialog.prompt()
      .title('Enter Email Address To Add')
      .placeholder('email@host.tld')
      .targetEvent(ev)
      .ok('Enter')
      .cancel('Cancel');

    $mdDialog.show(confirm).then(function(result) {
      console.log("User Added: "+ result);
    }, function() {
    });
  };
};
export default [ '$mdDialog', ManageController ];
