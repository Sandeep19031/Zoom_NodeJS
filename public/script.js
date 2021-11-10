const socket = io('/')
const videoGrid = document.getElementById('video-grid');

var myPeer = new Peer(undefined, {
    path: '/peerjs', 
    host: '/',
    port: '443',
    
})
const myVideo = document.createElement('video');
myVideo.muted = true;

let myVideoStream;
var getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.mediaDevices.enumerateDevices;
navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true
}).then( stream => {
    addVideoStream(myVideo, stream);
    myVideoStream = stream;
    socket.on('user-connected', (userId) => {
        connectToNewUser(userId, stream);
    })
    
})


myPeer.on('open', id => {
    socket.emit('join-room', ROOM_ID, id);
})
myPeer.on('call', call => {
    
    getUserMedia({video: true, audio: true}, function(stream) {
        call.answer(stream); 
        const video = document.createElement('video');
       
        call.on('stream', function(userVideoStream) {
            console.log('Failed to get local stream3');
          addVideoStream(video, userVideoStream);
        });
      }, function(err) {
        console.log('Failed to get local stream' ,err);
      });
})

const connectToNewUser = (userId, stream) => {
    var call = myPeer.call(userId,stream);
    
    const video = document.createElement('video');
   call.on('stream', userVideoStream =>{
  
       addVideoStream(video, userVideoStream)
   })
 
    
}
const addVideoStream = ( video, stream) => {
    video.srcObject = stream;
    
    video.addEventListener('loadedmetadata' , () => {
        video.play()
    })
    videoGrid.append(video);
} 
let text = $('input')
$('html').keydown((e) => {
    if(e.which == 13 && text.val().length != 0){
        console.log(text.val())
        socket.emit('message',text.val())
        text.val('')
    }
})
socket.on('createMessage', message => {
    $('ul').append(`<li class="message"><b>User</b><br/>${message}</li>`);
    scrollBottom()
})

const scrollBottom = () => {
    const d = $('.main_chat_window');
    d.scrollTop(d.prop("scrollHeight"));
}

const muteUnmute = () => {
    const enabled = myVideoStream.getAudioTracks()[0].enabled;
    if(enabled) {
        myVideoStream.getAudioTracks()[0].enabled = false;
        setUnmuteButton();
    }else{
        setMuteButton();
        myVideoStream.getAudioTracks()[0].enabled = true;
    }
}

const setMuteButton = () => {
    const html = `<i class="fas fa-microphone"></i><span>Mute</span>`
    document.querySelector('.main_mute_button').innerHTML = html;
}
const setUnmuteButton = () => {
    const html = `<i class="unmute fas fa-microphone-slash"></i><span>Unmute</span>`
    document.querySelector('.main_mute_button').innerHTML = html;
}

const playStop = () => {
    console.log('object');
    let enabled = myVideoStream.getVideoTracks()[0].enabled;
    if(enabled){
        myVideoStream.getVideoTracks()[0].enabled= false;
        setPlayVideo();
    }else{
        setStopVideo();
        myVideoStream.getVideoTracks()[0].enabled = true;
    }
}
const setPlayVideo = () => {
    const html = `<i class="stop fas fa-video-slash"></i><span>Play Video</span>`
    document.querySelector('.main_video_button').innerHTML = html;
}
const setStopVideo = () => {
    const html = `<i class="play fas fa-video"></i><span>Stop Video</span>`
    document.querySelector('.main_video_button').innerHTML = html;
}