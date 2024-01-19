$guess = $('#btnSubmit')
$correctGuess = $('#displayGuess')
$timer = $('#timer')
$usedwords = $('#words')
$wordslist=$('#words-list')
$score = $('#score')
$timesPlayed = $('#timesPlayed')
$topScore = $('#topScore')

const used_words_list = []

let scoreCount = 0
let countdown = 60

$(document).ready(getScore)

$(document).ready(setTimeout(stopGame, 60000))

setInterval(updateTime, 1000)

async function getScore(){
    response = await axios.get("http://127.0.0.1:5000/get_score")
    $timesPlayed.html(`You've played ${response.data['playTimes']} times`)
    $topScore.html(`Your top score is ${response.data['score']}`)
}

async function stopGame(){
   
    $guess.prop('disabled', true)

    response = await axios.post("http://127.0.0.1:5000/update_score", {score: scoreCount})
    $timesPlayed.html(`You've played ${response.data['playTimes']} times`)
    $topScore.html(`Your top score is ${response.data['score']}`)
}


function updateTime(){
    if (countdown == 0){
        clearInterval(updateTime)
        $timer.html(`Time's up!`)
    } else{
    countdown = countdown - 1
    $timer.html(`Time remaining is ${countdown}s`)
    }
}
 
$guess.on('click', async function(e){
    e.preventDefault()
    guessWord = document.querySelector('#inputGuess').value
    response = await axios.post("http://127.0.0.1:5000/check_word", {word: guessWord})
    $correctGuess.html("")

    if(response.data['message'] == "WORKS!"){
        
        if(used_words_list.includes(guessWord)){
            $correctGuess.append(`${guessWord} is already used`)
        }
        else{
            used_words_list.push(guessWord)
            $correctGuess.append(`${guessWord} works`)
            $wordslist.append($(`<ul>${guessWord}</ul>`))
            scoreCount = scoreCount + guessWord.length
            $score.html('Score is ' + scoreCount)
        }
    } 
    else if(response.data['message'] == "NOT A WORD"){
        $correctGuess.append(`${guessWord} is not a word`)
    } 
    else{
        $correctGuess.append(`${guessWord} is not on the board`)
    }
})
