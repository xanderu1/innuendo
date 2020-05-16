$(document).ready(function() {
   var socket = io();
   var inetChannel = 1;
   var radioLink = "./hammer.wma";
   var maxRadioChannel = 1;
   var maxNrOfFiles = 0;
   var mediaIndex = 0;
   var mediaUrl = "/home/pi/innuendo/nasservers/Music/";
   var mediaFileUrl = "./hammer.wma";
   var mediaLinks = new Array(10);
   for(index = 0; index < 10; index++)
      mediaLinks[index] = new Array(3);

   function showMenu(menu) {
      // Show menu tab
      $('.PanelPage').hide();
      $('.FooterPage').hide();
      $('#VolumePage0').hide();
      switch(menu) {
         case 0:
            // Introduction page
            $('#PanelPage0').show();
            $('#FooterPage0').show();
            break;
         case 1:
            // Innuendo home page
            $('#PanelPage1').show();
            $('#FooterPage1').show();
            $('#VolumePage0').show();
            break;
         case 2:
            // Media-player page
            $('#PanelPage2').show();
            $('#FooterPage2').show();
            $('#VolumePage0').show();
            break;
         case 3:
            // Internet-radio page
            $('#PanelPage3').show();
            $('#FooterPage3').show();
            $('#VolumePage0').show();
            break;
         case 4:
            // DVD-player page
            $('#PanelPage4').show();
            $('#FooterPage4').show();
            $('#VolumePage0').show();
            break;
         case 5:
            // Auxiliary page
            $('#PanelPage5').show();
            $('#FooterPage5').show();
            $('#VolumePage0').show();
            break;
         default:
            // default introduction page.
            $('#PanelPage0').show();
            $('#FooterPage0').show();
            $('#VolumePage0').show();
      }
   }

   function sourceName(source) {
      // returns source number in text
      var SourceText = "Innuendo";
      switch(source) {
         case 1:
            SourceText = "Media-Player";
            break;
         case 2:
            SourceText = "inet-Radio";
            break;
         case 3:
            SourceText = "DVD-Player";
            break;
         case 4:
            SourceText = "Auxiliary";
            break;
         default:
            SourceText = "Unknown";
      }
      return SourceText;
   }

   function doorStatus(door) {
      // returns door status in text
      var DoorText = "Error";
      switch(door) {
         case 1:
            DoorText = "Open";
            break;
         default:
            DoorText = "Closed";
      }
      return DoorText;
   }

   function powerStatus(power) {
      // return preamp power status in text
      var PowerText = "Error";
      switch(power) {
         case 1:
            PowerText = "On";
            break;
         default:
            PowerText = "Standby";
      }
      return PowerText;
   }

   function muteStatus(mute) {
      // returns mute status in text.
      var MuteText = "Error";
      switch(mute) {
         case 1:
            MuteText = "On";
            break;
         default:
            MuteText = "Mute";
      }
      return MuteText;
   }

   //Step back one folder
   function DirectoryUp( Url ) {
      var tmp = "./"
      if( Url.length > 1 ) {
         tmp = Url.substring(0, Url.length - 1)
         while(tmp.length > 1 && tmp[tmp.length - 1] != '/') {
            tmp = tmp.substring(0, tmp.length - 1)
         }
      }
      return tmp
   }

   //retrieve radio channel from radio.php.
   function getRadioChannel(inetChannel) {
      $.post("./radio.php", { start: inetChannel },
         function(data, status){
            jsonObj = JSON.parse(data);
            if("link" in jsonObj && "maxRadioLink" in jsonObj) {
                $("#radiochannel").text("[" + inetChannel + "/" + jsonObj.maxRadioLink + "] - " + jsonObj.title);
                radioLink = jsonObj.link;
                maxRadioChannel = parseInt(jsonObj.maxRadioLink);
            } else {
                $("#radiochannel").text("[1/1] - No Channels");
            }
         }).fail(function() {
            $("#radiochannel").text("[1/1] - No Channels");
         });
   }

   //retrieve media files from media.php.
   function getMediaFiles( page, Url ) {
      $.post("./media.php", { start: page * 10 + 1, length: 10, link: Url },
         function(data, status){
            jsonObj = JSON.parse(data);
            if("maxLength" in jsonObj) {
                maxNrOfFiles = parseInt(jsonObj.maxLength);
            }
            if("list" in jsonObj) {
                list = jsonObj.list;
                for (i = 0; i < 10; i++) {
                    tmp = 'File' + i.toString();
                    if(i < list.length) {
                        document.getElementById( tmp ).value = list[i].title;
                        mediaLinks[i][0] = list[i].title;
                        mediaLinks[i][1] = list[i].directory;
                        mediaLinks[i][2] = list[i].link;
                        document.getElementById( tmp ).style.visibility = "visible";
                        if(list[i].directory == "True") {
                            document.getElementById( tmp ).style.backgroundColor = "#ffff00AA";
                        } else {
                            document.getElementById( tmp ).style.backgroundColor = "#00ffffAA";
                        }
                    } else {
                        document.getElementById( tmp ).value = "";
                        document.getElementById( tmp ).style.visibility = "hidden";
                    }
                }
            }
         })
   }

   //Receiving preampfeedback data from webserver
   socket.on('preampfeedback', function(message) {
      $('#VolumeFB').text(message.VolumeFB);
      $('#BassFB').text(message.BassFB);
      $('#MiddleFB').text(message.MiddleFB);
      $('#TrebbleFB').text(message.TrebbleFB);
      $('#HeaderPage1').text(sourceName(message.SelectFB));
   });

   //Receiving powerfeedback data from webserver
   socket.on('powerfeedback', function(message) {
      $('#FrontDoorFB').text(doorStatus(message.FrontDoorFB));
      $('#PreampPowerFB').text(powerStatus(message.PreampPowerFB));
      $('#LineOutputFB').text(muteStatus(message.LineOutputFB));
   });

   $('#VolumeUp').click(function () {
      socket.emit('preampcontrol', {"VolumeCtrl": +1});
   });

   $('#VolumeDown').click(function () {
      socket.emit('preampcontrol', {"VolumeCtrl": -1});
   });

   $('#BassUp').click(function () {
      socket.emit('preampcontrol', {"BassCtrl": +1});
   });

   $('#BassDown').click(function () {
      socket.emit('preampcontrol', {"BassCtrl": -1});
   });

   $('#TrebbleUp').click(function () {
      socket.emit('preampcontrol', {"TrebbleCtrl": +1});
   });

   $('#TrebbleDown').click(function () {
      socket.emit('preampcontrol', {"TrebbleCtrl": -1});
   });

   $('#MiddleUp').click(function () {
      socket.emit('preampcontrol', {"MiddleCtrl": +1});
   });

   $('#MiddleDown').click(function () {
      socket.emit('preampcontrol', {"MiddleCtrl": -1});
   });

   $('#FrontDoorUp').click(function () {
      socket.emit('powercontrol', {"FrontDoorCtrl": 1});
   });

   $('#FrontDoorDown').click(function () {
      socket.emit('powercontrol', {"FrontDoorCtrl": -1});
   });

   $('#PreampPowerUp').click(function () {
      socket.emit('powercontrol', {"PreampPowerCtrl": 1});
   });

   $('#PreampPowerDown').click(function () {
      socket.emit('powercontrol', {"PreampPowerCtrl": -1});
   });

   $('#LineOutputUp').click(function () {
      socket.emit('powercontrol', {"LineOutputCtrl": 1});
   });

   $('#LineOutputDown').click(function () {
      socket.emit('powercontrol', {"LineOutputCtrl": -1});
   });

   $('#play4').click(function () {
      socket.emit('preampcontrol', {"SelectCtrl": 3});
   });

   $('#play5').click(function () {
      socket.emit('preampcontrol', {"SelectCtrl": 4});
   });

   // main page
   $('#Select1').click(function () {
      getMediaFiles( mediaIndex, mediaUrl );
      showMenu(2);
   });

   $('#Select2').click(function () {
      getRadioChannel(inetChannel);
      showMenu(3);
   });

   $('#Select3').click(function () {
      showMenu(4);
   });

   $('#Select4').click(function () {
      showMenu(5);
   });

   $('#TerminateAudio').click(function () {
      socket.emit('preampcontrol', {"TerminateAudio": true});
   });

   $('#TerminatePower').click(function () {
      socket.emit('powercontrol', {"TerminatePower": true});
   });

   $('.HomeBtn').click(function() {
      showMenu(1);
   });

   $('#HomeLink1').click(function() {
      showMenu(0);
   });

   //media player page
   $('#play2').click(function () {
      socket.emit('preampcontrol', {"SelectCtrl": 1});
      socket.emit('mediaplayerctrl', { "cmd": "play", "url": mediaFileUrl});
   });

    $("#next2").click(function() {
      mediaIndex = mediaIndex + 1;
      if(mediaIndex > maxNrOfFiles / 10) {
         mediaIndex = Math.trunc(maxNrOfFiles / 10);
      }
      getMediaFiles( mediaIndex, mediaUrl );
    });

    $("#previous2").click(function() {
      mediaIndex = mediaIndex - 1;
      if(mediaIndex < 0) {
         mediaIndex = 0;
      }
      getMediaFiles( mediaIndex, mediaUrl );
   });

   $("#DirectoryUp2").click(function() {
      mediaIndex = 0;
      mediaUrl = DirectoryUp( mediaUrl );
      getMediaFiles( mediaIndex, mediaUrl );
   });

   $("#stop2").click(function() {
      socket.emit('mediaplayerctrl', { "cmd": "stop" });
   });

   $(".FileBtn").click(function() {
      var id = parseInt( this.id[4] );
      if( mediaLinks[id][1] != "True" ) {
         document.getElementById("AudioFile").value = mediaLinks[id][0];
         mediaFileUrl = mediaLinks[id][2];
      } else {
         mediaIndex = 0;
         mediaUrl = mediaLinks[id][2];
         getMediaFiles( mediaIndex, mediaUrl )
      }
   });

   //inet radio page
   $('#play3').click(function () {
      socket.emit('preampcontrol', {"SelectCtrl": 2});
      socket.emit('mediaplayerctrl', { "cmd": "play", "url": radioLink});
   });

   $("#next3").click(function() {
      inetChannel = inetChannel + 1;
      if(inetChannel > maxRadioChannel) {
         inetChannel = 1;
      }
      getRadioChannel(inetChannel);
   });

   $("#previous3").click(function() {
      inetChannel = inetChannel - 1;
      if(inetChannel < 1) {
         inetChannel = maxRadioChannel;
      }
      getRadioChannel(inetChannel);
   });

   $("#stop3").click(function() {
      socket.emit('mediaplayerctrl', { "cmd": "stop" });
   });

});
