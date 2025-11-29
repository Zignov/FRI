select jid, ime
from Jadralec
where starost > 50;

select distinct barva
from coln
where dolzina between 35 and 40;

select coln.cid, coln.ime
from coln, Rezervacija, jadralec
where coln.cid = rezervacija.cid and rezervacija.jid = jadralec.jid
	and Jadralec.ime = "lojze";
    
select *
from coln, Rezervacija
where coln.cid = rezervacija.cid;

select Jadralec.ime, coln.ime
from coln, Rezervacija, Jadralec
where coln.cid = Rezervacija.cid and Rezervacija.jid = Jadralec.jid;

select distinct j.ime
from coln c, rezervacija r, Jadralec j
where c.cid = r.cid and r.jid = j.jid and c.barva = "rdeca";

select j1.ime, j2.ime, j1.rating
from jadralec j1, jadralec j2
where j1.rating = j2.rating and j1.jid < j2.jid
order by j1.rating desc;

select ime
from jadralec
where ime like "b$";

select j.ime, j.starost
from jadralec j
where ime regexp '^B....+$' or ime regexp 'o$';

#Employees
select last_name
from employees
where last_name like '%ski%';

select dept_name
from departments;

select distinct e.first_name, e.last_name
from employees e, salaries s
where e.emp_no = s.emp_no and s.salary > 70000;

select distinct e.first_name, e.last_name
from employees e, titles t
where e.emp_no = t.emp_no and title = "Senior Staff";

select last_name
from employees
where last_name like "Pea%";

select e.last_name, t.title
from employees e, titles t
where last_name like "Pea%" and e.emp_no = t.emp_no;

#Travian

select *
from aliansa
where alliance like "%mgp%";

select distinct tribe
from pleme;

select distinct i.player
from igralec i, naselje n
where i.pid=n.pid and n.population >= 1000;

select village
from igralec i, naselje n
where i.pid=n.pid and i.player = "Ronin";