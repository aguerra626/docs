USE msdb;

SELECT 
    j.name AS JobName,
    s.name AS ScheduleName,
    js.next_run_date,
    js.next_run_time,
    st.step_id,
    st.step_name,
    st.command,
    st.on_success_action,
    st.on_fail_action
FROM 
    dbo.sysjobs j
JOIN 
    dbo.sysjobschedules js ON j.job_id = js.job_id
JOIN 
    dbo.sysschedules s ON js.schedule_id = s.schedule_id
JOIN 
    dbo.sysjobsteps st ON j.job_id = st.job_id
ORDER BY 
    j.name, 
    st.step_id;
