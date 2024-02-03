#include <iostream>
#include <boost/algorithm/string.hpp>
using namespace std;
using namespace boost;

int main()
{
	string fio= "    Inyakin Roman Olegovich     ";
	trim(fio);
	string surname, name, grandname;
	//Surname name and grandname
	surname = erase_tail_copy(fio, fio.size()-fio.find(' '));
	name = erase_head_copy(fio,fio.find(' ')+1);
	grandname=erase_head_copy(name,name.find(' ')+1);
	erase_tail(name,name.size()-name.find(' '));
    cout<<fio<<endl<< surname<<endl<<name<<endl<<grandname<<endl;
	//end
	string fio_in_upper_case=to_upper_copy(fio);
	string fio_in_lower_case=to_lower_copy(fio);
	cout<<fio_in_upper_case<<"   "<<fio_in_lower_case<<endl;
	cout<<find_first(fio,name)<<endl;
	string new_surname;
	cout<<"New surname: ";
	cin>>new_surname;
	string new_fio=ireplace_first_copy(fio,surname,new_surname);
	cout<<new_fio<<endl;
	cout<<"FIO "<<(all(fio,is_upper()) ? "was":"wasn't")<<" written in upper case"<<endl;
	cout<<"FIO "<<(all(fio,is_lower()) ? "was":"wasn't")<<" written in lower case"<<endl;
	return 0;
}

