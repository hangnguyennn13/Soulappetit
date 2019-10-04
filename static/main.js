
$(function() {

    $("#file").on('change', function(event) {
        let image = document.getElementById('output');
        image.src = URL.createObjectURL(event.target.files[0]);
        $('#myButton, .section-input-firstname').removeClass('hidden')
    }); 

    $("#myButton").on('click', function(e)
    {
        // e.preventDefault();
        // if ($('.input-firstname').val() != '' ) {
        // $('#form-predict-correction').trigger('submit')
        // }
        $('#form-predict-correction').trigger('submit')
    });
    function renderMusic(music){
        let name = music[1] + " - " + music[2]; 
        return `
        <li>
            <button class="myBtn" id=${music[3]} onclick="newMusic" type="button">${name}</button>
        </li>
        `
    }
    function renderMusic2(music,index, arr){
        let name = "s"+index.toString();
        console.log(name);
        return `
        <div id =${name} class="hidden">
            <div id="${music[3]}" style="display: flex; flex-direction: column;" >
                <h2 style="color:white">${music[1]}</h2>
                <p style="color:white">It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.</p>
                <p style="color:white">The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to . </p> 
                <div id ="playlist">
                    <button id=${index-1} class="preBtn">Previous</button>
                    <button id=${music[3]} class="curBtn">Play</button>
                    <button id=${index+1} class="nextBtn">Next</button>
                </div>
            </div>
        </div>
       
        `
    }

    $('#form-predict-correction').on('submit', function(e) {
        e.preventDefault();
        let my_form = document.getElementById('form-predict-correction')
        let form_data = new FormData(my_form);
        
        let image = document.getElementById('output');
        
        console.log(form_data);

        $.ajax({
            type: 'POST',
            url: '/upload/',
            processData: false,
            contentType: false,
            data: form_data,
            success: function(data) {
                $('#form-predict-correction .button,.section-input-firstname').addClass('hidden')
                // $('#playerDetail').removeClass("hidden")
                console.log()
                $('#output').attr('src', 'data:image/jpg;base64,' + data['img'])
                // initYoutube();
                $('#player').removeClass('hidden')
                player.loadVideoById(data['videoId'])
                player.playVideo()
                console.log(data['videoId'])
                
                // const songs = data['song'];
                // console.log(data['song'])
                // const songsHTML = songs.map(renderMusic).join('');
                // document.getElementById('newsList').innerHTML = songsHTML;

                
                // document.addEventListener('click', function(e){
                //     if(e.target.tagName=="BUTTON"){
                //         player.loadVideoById(e.target.id);
                //         player.playVideo();
                //     }
                //   })

                const songs2 = data['song'];
                console.log(data['song'])
                const songsHTML2 = songs2.map(renderMusic2).join('');
                document.getElementById('playerDetail').innerHTML = songsHTML2;
                
                $('#s0').removeClass('hidden');

                document.addEventListener('click', function(e){
                    if(e.target.tagName=="BUTTON"){
                        if(e.target.className =="preBtn"){
                            
                            let preId = parseInt(e.target.id, 10);
                            if(preId>=0){
                                
                                let currId = preId+1;
                                currId = "s"+currId.toString();

                                // let oldSong = document.getElementById(currId);
                                // oldSong.addClass("hidden");
                                $("#"+currId).addClass("hidden");

                                let newId = "s"+preId.toString();
                                // let newSong = document.getElementById(newId);
                                // newSong.removeClass("hidden");
                                $("#"+newId).removeClass("hidden");

                            }
                        }
                        if(e.target.className =="nextBtn"){
                            console.log("nextButton");
                            let nextId = parseInt(e.target.id, 10);
                            if(nextId<=9){
                                let currId = nextId-1;
                                currId = "s"+currId.toString();
                                console.log(currId);
                                // let oldSong = document.getElementById(currId);
                                // oldSong.addClass("hidden");
                                $("#"+currId).addClass("hidden");

                                let newId = "s"+nextId.toString();
                                // let newSong = document.getElementById(newId);
                                // newSong.removeClass("hidden");

                                $("#"+newId).removeClass("hidden");
                                console.log(newId);

                            }
                        }
                        if(e.target.className =="curBtn"){
                            
                            player.loadVideoById(e.target.id);
                            player.playVideo();

                        
                        }
                    }
                })

            }
        });
    });

    
});

