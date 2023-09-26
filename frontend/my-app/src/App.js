import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  header: {
    fontSize: '4rem',
    fontWeight: 'bold',
    color: '#3f51b5',  // Material-UIのデフォルトのプライマリカラー
    marginBottom: '20px',
    textShadow: '2px 2px 4px #000000',  // テキストに影をつける
  },
});

function App() {
  const classes = useStyles();

  const [formData, setFormData] = useState({
    job: '',
    position: '',
    mission: '',
    role: '',
    appeal: '',
    skill: '',
  });
  const [response, setResponse] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

const handleSubmit = async () => {
  // 既存のresponseをクリア
  setResponse(null);

  console.log("Sending data:", formData);  // 送信するデータをコンソールに出力
  try {
    const res = await axios.post('http://127.0.0.1:8000/make_resume/', formData);
    setResponse(res.data);
  } catch (error) {
    console.error('There was an error!', error);
  }
};


  return (
    <div>
      <Typography variant="h2" className={classes.header}> Resume Maker </Typography>
      <TextField label="Job" variant="outlined" name="job" onChange={handleChange} />
      <TextField label="Position" variant="outlined" name="position" onChange={handleChange} />
      <TextField label="Mission" variant="outlined" name="mission" onChange={handleChange} />
      <TextField label="Role" style={{ width: '1000px'}} variant="outlined" name="role" onChange={handleChange} /><br></br>
      <TextField label="Appeal" style={{ width: '1900px'}} variant="outlined" name="appeal" onChange={handleChange} /><br></br>
      <TextField label="skill" style={{ width: '1900px'}} variant="outlined" name="skill" onChange={handleChange} /><br></br>
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        レジュメ生成！
      </Button>
      {response && (
        <div>
          <br></br>
          <Typography variant="h6">出力結果 [{response.status} 処理時間:{response.elapse_time}]</Typography><br></br>
          <TextField multiline rows={2} style={{ width: '1900px'}} label="最初に生成したレジュメ" variant="outlined" value={response.base_resume_text} InputProps={{readOnly: true,}}/><br/><br/>
          <TextField multiline rows={10} style={{ width: '1900px'}} label="より魅力的にするアドバイス" variant="outlined" value={response.advice_text} InputProps={{readOnly: true,}}/><br/><br/>
          <TextField multiline rows={12} style={{ width: '1900px'}} label="最終的なレジュメ" variant="outlined" value={response.final_resume_text} InputProps={{readOnly: true,}}/>
        </div>
      )}
    </div>
  );
}

export default App;