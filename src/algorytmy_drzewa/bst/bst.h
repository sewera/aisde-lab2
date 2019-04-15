//
//  Created by Adam Wojtasik on 03/04/2017.
//  Copyright © 2017 Institute of Microelectronics and Optoelectronics. All rights reserved.
//

#ifndef bst_h
#define bst_h

#include "tablica.h"
#include "vertex.h"



//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Klasa reprezentująca węzeł w drzewie BST
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
template <typename RECORD>
class VertexBST : public Vertex{
	RECORD value;
public:
	
	VertexBST(RECORD& v, TreeHead* org = nullptr) : Vertex(org), value(v){}
	
	RECORD& getKey(){ return value; }
	
	bool addNewVertex(Vertex*);
	Vertex* createEmptyVertex(TreeHead* = nullptr);
	bool isEmpty(){ return value.isEmpty(); }
	
	// Poszukiwanie węzła z rekordem o tamim samym kluczu jak dany
	VertexBST* find(RECORD& key){
		if(key < value){
			if(left == nullptr) return nullptr;
			else return dynamic_cast<VertexBST*>(left)->find(key);
		}
		else if(key > value){
			if(right == nullptr) return nullptr;
			else return dynamic_cast<VertexBST*>(right)->find(key);
		}
		else return this;
	}
	
	// Wydruk zawartości rekordu należącego do węzła
	void display(std::string, int form){ value.display(form); }
	
	// Przeciążone operatory porównań
	bool operator >  (Vertex& sec) const{ return value >  dynamic_cast<VertexBST&>(sec).value; }
	bool operator >= (Vertex& sec) const{ return value >= dynamic_cast<VertexBST&>(sec).value; }
	bool operator <  (Vertex& sec) const{ return value <  dynamic_cast<VertexBST&>(sec).value; }
	bool operator <= (Vertex& sec) const{ return value <= dynamic_cast<VertexBST&>(sec).value; }
	bool operator == (Vertex& sec) const{ return value == dynamic_cast<VertexBST&>(sec).value; }
	bool operator != (Vertex& sec) const{ return value != dynamic_cast<VertexBST&>(sec).value; }
	
	template <typename> friend class BstHead;
	
	void rotateLeft(){
		if(right != nullptr){
			Vertex* rightDesc = right;
			
			rightDesc->setFather(father);
			if(father == nullptr) origin->setRoot(rightDesc);
			else{
				if(father->getLeft() == this) father->setLeft(rightDesc);
				else father->setRight(rightDesc);
			}
			
			right = rightDesc->getLeft();
			if(right!= nullptr) right->setFather(this);
			
			rightDesc->setLeft(this);
			father = rightDesc;
		}
	}
	
	void rotateRight(){
		if(left != nullptr){
			Vertex* leftDesc = left;
			
			leftDesc->setFather(father);
			if(father == nullptr) origin->setRoot(leftDesc);
			else{
				if(father->getRight() == this) father->setRight(leftDesc);
				else father->setLeft(leftDesc);
			}

			left = leftDesc->getRight();
			if(left != nullptr) left->setFather(this);
			
			leftDesc->setRight(this);
			father = leftDesc;
		}
	}

	
};
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Dodefiniowanie metod czystoabstrakcyjnych z klasy Vertex
template <typename RECORD>
bool VertexBST<RECORD>::addNewVertex(
	Vertex* newVertex
){
	bool ret = true;
	if((*this) > (*newVertex)){
		if(left == nullptr) { left = newVertex; newVertex->setFather(this); ret = false; }
		else return left->addNewVertex(newVertex);
	}
	else if((*newVertex) > (*this)){
		if(right == nullptr) { right = newVertex; newVertex->setFather(this); ret = false; }
		else return right->addNewVertex(newVertex);
	}
	return ret;
}
template <typename RECORD>
Vertex* VertexBST<RECORD>::createEmptyVertex(
    TreeHead* org
){
	RECORD temp(true);
	return new VertexBST<RECORD>(temp);
}
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// klasa reprentująca całe drzewo BST (tzw. głowa)
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
template <typename RECORD>
class BstHead : public TreeHead {
public:
    BstHead<RECORD>(){}

// Przeciążony operator dodawania do drzewa nowego węzła
    bool operator += (RECORD& val){
        bool ret = true;
        VertexBST<RECORD>* rob = new VertexBST<RECORD>(val,this);

        if(root == nullptr) { root = rob; ret = false; }
        else{
            ret = root->addNewVertex(rob);
            if(ret) delete rob;
        }
        return ret;
    }

// wewnętrzne metody pomocnicze
protected:
	void complete(){ if(root != nullptr){ int height = root->calculateHeight(); dynamic_cast<VertexBST<RECORD>*>(root)->complete(height,1); }}
	void clean(){ if(root != nullptr) dynamic_cast<VertexBST<RECORD>*>(root)->clean(); }
};
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// klasa reprentująca całe drzewo BST z danymi typu całkowitego
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BstHeadINT : public BstHead<ObjectINT>, public ArrayINT{
	int format;
public:
    BstHeadINT(long num) : ArrayINT(num) {
		if(num < 10) format = 2;
		else if(num < 100) format = 3;
		else if(num < 1000) format = 4;
		else format = 0;
	}
    ~BstHeadINT(){ }

// Budowanie drzewa z rekordów umieszczonych w tablicy
    void createTree(){ for(Iterator i = firstIndex(); i <= lastIndex(); ++i) (*this) += array[i]; }

// Wydruk drzewa na konsolę
// flaga comp decyduje o tym, czy wydruk jest pełny (drzewo pełne z kreskami zamiast "pustych" węzłów, czy skrócony (tylko istniejące węzły)
	void wypiszNaKonsole(bool comp = false){
		if(root == nullptr) cout << "drzewo jest puste" << endl;
		else{
			if(format < 2) throw Error(ERR_LargePrint);
			if(comp) complete();
			root->displayTree(0,format);
			if(comp) clean();
		}
	}
};
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#endif /* bst_h */

