<template>
<div class="bg-dark text-white">

    

    <span class="font-weight-bold  text-lg-left">Check Text:</span>

    <b-container class="bv-example-row ">
    <b-row>   
        <b-form-textarea 
            id="textareaa"
            v-model="text"
            placeholder="Type type something"
            rows="6"
            max-rows="12"
            :disabled="loading || (file != null)" />
    </b-row>
    Or
    <b-row>
        <b-form-file
            v-model="file"
            placeholder="Choose/Drop a file"
            drop-placeholder="Drop file here"
            accept=".txt"
            :disabled="loading" />
    </b-row>
    <br> <br>
    <b-row>
        <b-col>
             <b-button size="lg" variant="outline-light" v-on:click="send"> Submit</b-button> 
        </b-col>
        <b-col> 
            <b-button size="lg" variant="outline-light" v-on:click="clear">Clear</b-button>   
        </b-col>
        
    </b-row>

    <b-row>
        <b-col>
            <p class="text-center" v-if="bill != 0">Bill: ${{bill}}</p>
        </b-col>
    </b-row>

    <br> <br>
    </b-container>
    
    <div class="bg-success text-white">
    <b-container class="bg-red text-white">
        <b-row>
            <b-col>

            <div v-show="loading">
                <b-spinner big ></b-spinner> 
                <p>Sending</p> 
                
            </div>


            </b-col>
        </b-row>
    </b-container>
   </div>

   <div v-if="errors != null" class="bg-white text-white">
    <b-container class="bg-red text-white">
        <b-row>
            <b-col>
                <h3> {{ errors.length }} errors found:</h3>
                <p>
                    <span v-for="i in showText.keys()" :key="i" :class="errors.indexOf(showText[i]) >= 0 ? 'text-danger' : 'text-dark'">{{ showText[i] }} </span>
                </p>
            </b-col>
        </b-row>
    </b-container>
   </div>

</div>
</template>

<script>
import Axios from 'axios'

export default {
    data() {
        return {
            file: null,
            text: '',
            loading : false,
            showText: [],
            errors: null,
            bill: 0,
        }
    },
  methods: {
    send: function () {
        this.visibility()

        let makeRequest = text => {
            console.log(text)

            // var formData = new FormData();
            // formData.append("text", text);

            var formData = { text: text }

            Axios.post('http://192.168.43.125:8000/spellcheck', JSON.stringify(formData), {
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                console.log(response.data);
                this.showText = text.split(' ');
                this.bill += response.data.bill;
                this.showErrors(response.data.wrong_words);
            });
        }

        if (this.file != null) {
            let reader = new FileReader()
            reader.readAsText(this.file, 'utf-8');
            reader.onload = (evt) => { makeRequest(evt.target.result) } 
        } else {
            makeRequest(this.text);
        }
    },
    visibility: function () {
        this.loading = true;
    },
    showErrors: function(errors) {
        console.log('showing errors: ', errors)
        this.loading = false;
        
        this.errors = errors
    },
    clear: function () {
        this.file = null;
        this.text = "";
        this.loading = false;
        this.errors = null;
    }

  }
}
</script>